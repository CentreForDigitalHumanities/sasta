import { Component, OnDestroy, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { faArrowRight, faCogs } from '@fortawesome/free-solid-svg-icons';
import { Corpus, Transcript } from '@models';
import { CorpusService, ParseService } from '@services';
import { MenuItem } from 'primeng/api';
import { interval, Observable, of, Subscription } from 'rxjs';
import { catchError, concatMap, startWith } from 'rxjs/operators';

@Component({
    standalone: false,
    selector: 'sas-process',
    templateUrl: './process.component.html',
    styleUrls: ['./process.component.scss'],
})
export class ProcessComponent implements OnInit, OnDestroy {
    corpus: Corpus;
    id: number;

    stepsItems: MenuItem[] = [
        { label: 'Convert to CHAT' },
        { label: 'Parse' },
        { label: 'Done' },
    ];
    stepsIndex: number;
    processing = false;

    subscription$: Subscription;
    interval$: Observable<number> = interval(2000);

    faCogs = faCogs;
    faArrowRight = faArrowRight;

    constructor(
        private route: ActivatedRoute,
        private corpusService: CorpusService,
        private parseService: ParseService
    ) {
        this.route.paramMap.subscribe(
            (params) => (this.id = +params.get('id'))
        );
    }

    ngOnInit() {
        this.subscription$ = this.interval$
            .pipe(startWith(0))
            .subscribe(() => this.getCorpus());
    }

    ngOnDestroy() {
        this.subscription$.unsubscribe();
    }

    getCorpus(): void {
        this.corpusService.getByID(this.id).subscribe(
            (res) => {
                this.corpus = res;
            },
            (err) => console.error(err)
        );
    }

    async fullProcess(): Promise<void> {
        this.processing = true;
        this.stepsIndex = 0;
        this.corpusService
            .convertAll(this.corpus.id)
            .pipe(
                concatMap((_) =>
                    this.corpusService.parseAllAsync(this.corpus.id)
                ),
                catchError((err) => of('error', err))
            )
            .subscribe(
                (res) => {
                    console.error(res);
                    this.stepsIndex += 1;
                },
                (err) => {
                    console.error(err);
                    this.stepsIndex += 1;
                },
                () => {
                    this.processing = false;
                    // this.router.navigate([`/corpora/${this.corpus.id}`]);
                }
            );
    }

    fullSingle(transcript: Transcript): void {
        this.parseService.fullProcess(transcript).subscribe(
            (next) => console.log(next),
            (err) => console.error(err)
        );
    }
}
