import {
    Component,
    DestroyRef,
    inject,
    OnInit,
    ViewChild,
} from '@angular/core';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { ActivatedRoute, Params, Router } from '@angular/router';
import { faUpload } from '@fortawesome/free-solid-svg-icons';
import { Corpus, ListedCorpus, UploadFile } from '@models';
import { CorpusService, UploadFileService } from '@services';
import { FileUpload, FileUploadHandlerEvent } from 'primeng/fileupload';
import { BehaviorSubject, forkJoin, Observable } from 'rxjs';
import { filter, switchMap, take, tap } from 'rxjs/operators';

@Component({
    selector: 'sas-upload',
    templateUrl: './upload.component.html',
    styleUrls: ['./upload.component.scss'],
})
export class UploadComponent implements OnInit {
    @ViewChild('fileInput') fileInput: FileUpload;
    readonly #destroyRef = inject(DestroyRef);
    loading$ = new BehaviorSubject<boolean>(false);

    files: File[];
    fileAccept = [
        '.cha',
        '.txt',
        '.docx',
        'application/msword',
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        '.zip',
        'application/zip',
        'application/x-zip-compressed',
        'multipart/x-zip',
    ].join(',');

    faUpload = faUpload;

    corpora$: Observable<ListedCorpus[]>;
    selectedCorpusId: number;

    corpusModalVisible: boolean = false;

    constructor(
        private router: Router,
        private corpusService: CorpusService,
        private uploadFileService: UploadFileService,
        private route: ActivatedRoute,
    ) {}

    ngOnInit() {
        this.corpusService.refresh();

        this.corpora$ = this.corpusService.getCorpora();

        this.route.queryParams
            .pipe(
                takeUntilDestroyed(this.#destroyRef),
                filter((params: Params) => !!params.corpus),
                switchMap((params: Params) =>
                    this.corpusService.getByID(params.corpus),
                ),
            )
            .subscribe((corpus: Corpus) => {
                this.selectedCorpusId = corpus.id;
            });
    }

    fullyFilled(): boolean {
        return this.selectedCorpusId && this.fileInput.files.length > 0;
    }

    openNewCorpus(): void {
        this.corpusModalVisible = true;
    }

    setCorpus(corpus: Corpus): void {
        this.corpusService.refresh();
        this.selectedCorpusId = corpus.id;
        this.corpusModalVisible = false;
    }

    onUpload(event: FileUploadHandlerEvent): void {
        // Triggered by PrimeNG file upload component
        this.files = event.files;
    }

    uploadFiles$(toCorpusId: number): Observable<UploadFile[]> {
        const uploadFiles: UploadFile[] = this.files.map((f: File) => ({
            name: f.name,
            content: f,
            status: 'uploading',
            corpus_id: toCorpusId,
        }));
        return forkJoin(
            uploadFiles.map((file) => this.uploadFileService.upload(file)),
        );
    }

    startUpload(): void {
        this.fileInput.upload();

        this.uploadFiles$(this.selectedCorpusId)
            .pipe(
                takeUntilDestroyed(this.#destroyRef),
                tap(() => this.loading$.next(true)),
            )
            .subscribe({
                next: (response) => {
                    this.loading$.next(false);
                    this.router.navigate([`/process/${response[0].corpus}`]);
                },
                error: (error) => {
                    console.error(error);
                    this.loading$.next(false);
                },
            });
    }
}
