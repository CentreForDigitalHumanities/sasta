import { Component, OnDestroy, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import {
    faArrowLeft,
    faDownload,
    faFile,
    faFileCode,
    faTrash,
    faUpload,
} from '@fortawesome/free-solid-svg-icons';
import { Corpus, Method, Transcript, TranscriptStatus } from '@models';
import { saveAs } from 'file-saver';
import { MessageService, SelectItemGroup } from 'primeng/api';
import { BehaviorSubject, Observable, Subject } from 'rxjs';
import { switchMap, takeUntil } from 'rxjs/operators';
import {
    AnalysisService,
    AnnotationOutputFormat,
    AnnotationsService,
    AuthService,
    CorpusService,
    MethodService,
    TranscriptService,
} from '@services';

import _ from 'lodash';

const XLSX_MIME =
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet';
const TXT_MIME = 'text/plain';

@Component({
    selector: 'sas-transcript',
    templateUrl: './transcript.component.html',
    styleUrls: ['./transcript.component.scss'],
})
export class TranscriptComponent implements OnInit, OnDestroy {
    id: number;
    transcript: Transcript;
    corpus: Corpus;

    tams: Method[];
    currentTam: Method;
    groupedTams: SelectItemGroup[];

    faTrash = faTrash;
    faFile = faFile;
    faFileCode = faFileCode;
    faArrowLeft = faArrowLeft;
    faDownload = faDownload;
    faUpload = faUpload;

    querying = false;

    displayCorrUpload = false;

    onDestroy$ = new Subject<boolean>();

    readonly TranscriptStatus = TranscriptStatus;

    // Checking for analysis in progress
    analysisInProgress$ = new BehaviorSubject<boolean>(false);
    resultsAvailable$ = new BehaviorSubject<boolean>(false);

    constructor(
        private transcriptService: TranscriptService,
        private corpusService: CorpusService,
        private methodService: MethodService,
        private analysisService: AnalysisService,
        private annotationsService: AnnotationsService,
        private router: Router,
        private route: ActivatedRoute,
        private messageService: MessageService,
        public authService: AuthService,
    ) {
        this.route.paramMap.subscribe(
            (params) => (this.id = +params.get('id')),
        );
    }

    hasLatestRun(): boolean {
        return !_.isNil(this.transcript.latest_run);
    }

    allowCorrectionUpload(): boolean {
        return (
            this.transcript.status === TranscriptStatus.PARSED &&
            this.hasLatestRun()
        );
    }

    allowCorrectionReset(): boolean {
        return this.hasLatestRun();
    }

    shouldAnalyse(): boolean {
        return (
            (_.isNil(this.transcript.latest_run) ||
                this.transcript.latest_run?.task_status === 'FAILURE' ||
                _.isNil(this.transcript.latest_run?.task_id)) &&
            this.transcript.latest_run?.task_status !== 'PENDING'
        );
    }

    ngOnInit() {
        this.loadData();
    }

    ngOnDestroy() {
        this.onDestroy$.next();
        this.onDestroy$.complete();
    }

    loadData(): void {
        this.transcriptService
            .getByID(this.id)
            .pipe(
                takeUntil(this.onDestroy$),
                // get transcript
                switchMap((t: Transcript) => {
                    this.transcript = t;
                    if (t.latest_run?.task_status === 'PENDING') {
                        this.analysisInProgress$.next(true);
                        this.pollResultsAvailable(t.latest_run.task_id);
                    } else {
                        this.analysisInProgress$.next(false);
                    }

                    this.resultsAvailable$.next(
                        t.latest_run?.results_available === true,
                    );
                    return this.corpusService.getByID(t.corpus); // get corpus
                }),
                switchMap((c: Corpus) => {
                    this.corpus = c;
                    return this.methodService.getMethod(c.default_method); // get default method
                }),
                switchMap((m: Method) => {
                    this.currentTam = m;
                    return this.methodService.getMethods(); // get all methods
                }),
            )
            .subscribe((tams: Method[]) => {
                this.tams = tams;
                this.groupedTams = this.methodService.groupMethods(
                    tams,
                    this.corpus.method_category,
                ); // group methods

                if (this.shouldAnalyse()) {
                    this.analyseAsync();
                }
            });
    }

    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    downloadFile(data: any, filename: string, mimetype: string): void {
        const blob = new Blob([data], { type: mimetype });
        saveAs(blob, filename);
    }

    private showSuccess(summary: string, detail = ''): void {
        this.messageService.add({ severity: 'success', summary, detail });
    }

    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    private showError(summary: string, err: any): void {
        console.error(err);
        this.messageService.add({
            severity: 'error',
            summary,
            detail: err.message,
            sticky: true,
        });
    }

    private performQueryAction(
        // eslint-disable-next-line @typescript-eslint/no-explicit-any
        obs$: Observable<any>,
        config: { filename: string; mime: string; successMsg: string },
        errorMsg: string,
    ): void {
        this.querying = true;
        obs$.pipe(takeUntil(this.onDestroy$)).subscribe({
            next: (response) => {
                this.downloadFile(response.body, config.filename, config.mime);
                this.showSuccess(config.successMsg);
                this.querying = false;
                this.loadData();
            },
            error: (err) => {
                this.showError(errorMsg, err);
                this.querying = false;
            },
        });
    }

    getResults(format: AnnotationOutputFormat): void {
        const configMap: Record<
            string,
            { filename: string; mime: string; successMsg: string }
        > = {
            xlsx: {
                filename: `${this.transcript.name}_SAF.xlsx`,
                mime: XLSX_MIME,
                successMsg: 'Annotation success',
            },
            cha: {
                filename: `${this.transcript.name}_annotated.cha`,
                mime: TXT_MIME,
                successMsg: 'Annotation success',
            },
            form: {
                filename: `${this.transcript.name}_${this.currentTam.category.name}_form.xlsx`,
                mime: XLSX_MIME,
                successMsg: 'Generated form',
            },
        };
        const config = configMap[format];
        if (!config) return;
        this.performQueryAction(
            this.analysisService.getResults(this.id, format),
            config,
            'Error generating results',
        );
    }

    downloadLatestAnnotations(): void {
        this.annotationsService
            .latest(this.id)
            .pipe(takeUntil(this.onDestroy$))
            .subscribe((res) => {
                this.downloadFile(
                    res.body,
                    `${this.transcript.name}_latest_SAF.xlsx`,
                    XLSX_MIME,
                );
            });
    }

    resetAnnotations(): void {
        this.annotationsService
            .reset(this.id)
            .pipe(takeUntil(this.onDestroy$))
            .subscribe(() => this.loadData());
    }

    analyseAsync(): void {
        this.analysisInProgress$.next(true);
        this.analysisService
            .createAnalysisTask(this.id, this.currentTam.id.toString())
            .subscribe({
                next: (taskID: string) => this.pollResultsAvailable(taskID),
                error: (err) =>
                    this.showError('Error creating analysis task', err),
            });
    }

    /**
     * Wait for async results to be available.
     */
    pollResultsAvailable(taskID: string): void {
        this.analysisService
            .pollAnalysisTask(taskID)
            .pipe(takeUntil(this.onDestroy$))
            .subscribe({
                next: () => {
                    this.showSuccess(
                        'Analysis success',
                        `Annotation completed for ${this.transcript.name}`,
                    );
                    this.loadData();
                },
                error: (err) =>
                    this.showError('Error analysing transcript', err),
            });
    }

    annotateTranscript(outputFormat: AnnotationOutputFormat): void {
        const configMap: Record<
            string,
            { filename: string; mime: string; successMsg: string }
        > = {
            xlsx: {
                filename: `${this.transcript.name}_SAF.xlsx`,
                mime: XLSX_MIME,
                successMsg: 'Annotation success',
            },
            cha: {
                filename: `${this.transcript.name}_annotated.cha`,
                mime: TXT_MIME,
                successMsg: 'Annotation success',
            },
        };
        const config = configMap[outputFormat];
        if (!config) return;
        this.performQueryAction(
            this.analysisService.annotate(
                this.id,
                this.currentTam.id.toString(),
                outputFormat,
            ),
            config,
            'Error querying',
        );
    }

    queryTranscript(): void {
        this.performQueryAction(
            this.analysisService.query(this.id, this.currentTam.id.toString()),
            {
                filename: `${this.transcript.name}_matches.xlsx`,
                mime: XLSX_MIME,
                successMsg: 'Querying success',
            },
            'Error querying',
        );
    }

    generateForm(): void {
        this.performQueryAction(
            this.analysisService.generateForm(
                this.id,
                this.currentTam.id.toString(),
            ),
            {
                filename: `${this.transcript.name}_${this.currentTam.category.name}_form.xlsx`,
                mime: XLSX_MIME,
                successMsg: 'Generated form',
            },
            'Error generating form',
        );
    }

    deleteTranscript(): void {
        const corpusId = this.corpus.id;
        this.transcriptService
            .delete(this.id)
            .pipe(takeUntil(this.onDestroy$))
            .subscribe({
                next: () => {
                    this.router.navigate([`/corpora/${corpusId}`]);
                    this.showSuccess('Removed transcript');
                },
                error: (err) =>
                    this.showError('Error removing transcript', err),
            });
    }

    chatFileAvailable(transcript: Transcript): boolean {
        return [TranscriptStatus.CONVERTED, TranscriptStatus.PARSED].includes(
            transcript.status,
        );
    }

    lassyFileAvailable(transcript: Transcript): boolean {
        return transcript.status === TranscriptStatus.PARSED;
    }

    showChat(): void {
        window.open(this.transcript.content, '_blank');
    }

    showLassy(): void {
        window.open(this.transcript.parsed_content, '_blank');
    }

    showCorrectedLassy(): void {
        window.open(this.transcript.corrected_content, '_blank');
    }

    showCorrectionsUpload(): void {
        this.displayCorrUpload = true;
    }

    onCorrectionsUploadClose(event: boolean): void {
        this.displayCorrUpload = event;
    }

    onAnnotationsUploaded(): void {
        this.loadData();
    }

    numUtterancesAnalysed(): number {
        // Count the number of utterances that will be analysed
        // Uses reduce to efficiently find the number
        return this.transcript.utterances.reduce(
            (total, utt) => (utt.for_analysis ? ++total : total),
            0,
        );
    }
}
