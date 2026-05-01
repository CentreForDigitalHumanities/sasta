import { Component, OnDestroy, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import {
    faCogs,
    faDownload,
    faPlus,
    faTrash,
} from '@fortawesome/free-solid-svg-icons';
import { Corpus, Method, Transcript } from '@models';
import {
    AuthService,
    CorpusService,
    MethodService,
    TranscriptService,
} from '@services';
import { saveAs } from 'file-saver';
import { MessageService, SelectItemGroup } from 'primeng/api';
import { interval, Observable, Subject } from 'rxjs';
import { startWith, switchMap, takeUntil } from 'rxjs/operators';

@Component({
    standalone: false,
    selector: 'sas-corpus',
    templateUrl: './corpus-detail.component.html',
    styleUrls: ['./corpus-detail.component.scss'],
})
export class CorpusComponent implements OnInit, OnDestroy {
    id: number;
    corpus: Corpus;

    tams: Method[];
    defaultTam: Method;
    groupedTams: SelectItemGroup[];

    faDownload = faDownload;
    faTrash = faTrash;
    faCogs = faCogs;
    faPlus = faPlus;

    interval$: Observable<number> = interval(5000);
    onDestroy$ = new Subject<void>();

    constructor(
        private corpusService: CorpusService,
        private transcriptService: TranscriptService,
        private methodService: MethodService,
        private route: ActivatedRoute,
        private messageService: MessageService,
        public authService: AuthService
    ) {
        this.route.paramMap.subscribe(
            (params) => (this.id = +params.get('id'))
        );
    }

    ngOnInit() {
        this.methodService
            .getMethods()
            .pipe(
                switchMap((methods) => {
                    this.tams = methods;
                    return this.corpusService.getByID(this.id);
                }),
                switchMap((c: Corpus) => {
                    this.groupedTams = this.methodService.groupMethods(
                        this.tams,
                        c.method_category
                    );
                    return this.interval$;
                }),
                startWith(0),
                takeUntil(this.onDestroy$)
            )
            .subscribe(() => {
                this.getCorpus();
            });
    }

    ngOnDestroy() {
        this.onDestroy$.next();
    }

    getCorpus(): void {
        this.corpusService
            .getByID(this.id)
            .pipe(takeUntil(this.onDestroy$))
            .subscribe((res) => {
                this.corpus = res;
                // retrieve default method
                if (res.default_method) {
                    this.methodService
                        .getMethod(res.default_method)
                        .pipe(takeUntil(this.onDestroy$))
                        .subscribe((tam) => (this.defaultTam = tam));
                }
            });
    }

    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    downloadFile(data: any, filename: string, mimetype: string): void {
        const blob = new Blob([data], { type: mimetype });
        saveAs(blob, filename);
    }

    deleteTranscript(transcript: Transcript): void {
        this.transcriptService
            .delete(transcript.id)
            .pipe(takeUntil(this.onDestroy$))
            .subscribe(
                () => {
                    this.getCorpus();
                    this.messageService.add({
                        severity: 'success',
                        summary: 'Removed transcript',
                        detail: '',
                    });
                },
                (err) => {
                    console.error(err);
                    this.messageService.add({
                        severity: 'error',
                        summary: 'Error removing transcript',
                        detail: err.message,
                        sticky: true,
                    });
                }
            );
    }

    changeDefaultMethod(): void {
        this.corpusService
            .setDefaultMethod(
                this.corpus.id,
                this.defaultTam ? this.defaultTam.id.toString() : null
            )
            .pipe(takeUntil(this.onDestroy$))
            .subscribe(
                () => {},
                (err) => {
                    console.error(err);
                    this.messageService.add({
                        severity: 'error',
                        summary: 'Error changing default method',
                        detail: err.message,
                        sticky: true,
                    });
                }
            );
    }

    downloadZip(): void {
        this.corpusService
            .downloadZip(this.corpus.id)
            .pipe(takeUntil(this.onDestroy$))
            .subscribe(
                (response) => {
                    this.downloadFile(
                        response.body,
                        `${this.corpus.name}.zip`,
                        'application/zip'
                    );
                    this.messageService.add({
                        severity: 'success',
                        summary: 'Downloaded corpus',
                        detail: '',
                    });
                },
                (err) => {
                    console.error(err);
                    this.messageService.add({
                        severity: 'error',
                        summary: 'Error downloading',
                        detail: err.message,
                        sticky: true,
                    });
                }
            );
    }
}
