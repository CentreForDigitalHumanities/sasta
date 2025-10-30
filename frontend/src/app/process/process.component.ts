import { Component, DestroyRef, inject, OnInit } from '@angular/core';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { ActivatedRoute } from '@angular/router';
import { faArrowRight, faCogs } from '@fortawesome/free-solid-svg-icons';
import { Corpus } from '@models';
import { CorpusService } from '@services';
import { interval, Observable, of, Subject } from 'rxjs';
import {
    catchError,
    concatMap,
    finalize,
    shareReplay,
    startWith,
    takeUntil,
} from 'rxjs/operators';

@Component({
    selector: 'sas-process',
    templateUrl: './process.component.html',
    styleUrls: ['./process.component.scss'],
})
export class ProcessComponent implements OnInit {
    readonly #destroyRef = inject(DestroyRef);

    corpus: Corpus;
    corpusId: number;

    processing = false;

    interval$: Observable<number> = interval(2000);

    faCogs = faCogs;
    faArrowRight = faArrowRight;

    corpus$: Observable<Corpus>;

    processingComplete$ = new Subject<boolean>();

    constructor(
        private route: ActivatedRoute,
        private corpusService: CorpusService,
    ) {
        this.route.paramMap.subscribe(
            (params) => (this.corpusId = +params.get('id')),
        );
    }

    ngOnInit() {
        this.corpus$ = this.interval$.pipe(
            takeUntilDestroyed(this.#destroyRef),
            startWith(0),
            takeUntil(this.processingComplete$),
            concatMap(() => this.corpusService.getByID(this.corpusId)),
            shareReplay(1),
        );

        this.corpus$.subscribe({
            next: (corpus: Corpus) => {
                if (this.shouldStartProcessing(corpus)) {
                    this.fullProcess(corpus);
                }
                if (this.shouldStopProcessing(corpus)) {
                    this.processingComplete$.next();
                }
            },
            error: console.error,
        });
    }

    fullProcess(corpus: Corpus): void {
        this.processing = true;
        this.corpusService
            .convertAll(corpus.id)
            .pipe(
                takeUntilDestroyed(this.#destroyRef),
                concatMap((convertedCorpus) =>
                    this.corpusService.parseAllAsync(convertedCorpus.id),
                ),
                finalize(() => (this.processing = false)),
                catchError((err) => of('error', err)),
            )
            .subscribe({ next: console.log, error: console.error });
    }

    private shouldStartProcessing(corpus: Corpus): boolean {
        return (
            !this.processing &&
            corpus.transcripts.some((t) => t.status_name === 'created')
        );
    }

    private shouldStopProcessing(corpus: Corpus): boolean {
        return corpus.transcripts.every(
            (t) =>
                t.status_name === 'parsed' ||
                t.status_name === 'parsing-failed' ||
                t.status_name === 'conversion-failed',
        );
    }
}
