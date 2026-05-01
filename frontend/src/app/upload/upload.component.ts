import { Component, OnInit, ViewChild } from '@angular/core';
import { ActivatedRoute, Params, Router } from '@angular/router';
import { faUpload } from '@fortawesome/free-solid-svg-icons';
import { Corpus, MethodCategory, UploadFile } from '@models';
import { CorpusService, MethodService, UploadFileService } from '@services';
import _ from 'lodash';
import { FileUpload, FileUploadHandlerEvent } from 'primeng/fileupload';
import { forkJoin, Observable } from 'rxjs';
import { concatMap, switchMap } from 'rxjs/operators';

@Component({
    standalone: false,
    selector: 'sas-upload',
    templateUrl: './upload.component.html',
    styleUrls: ['./upload.component.scss'],
})
export class UploadComponent implements OnInit {
    @ViewChild('fileInput') fileInput: FileUpload;

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

    newCorpusName: string;

    faUpload = faUpload;

    uploading: boolean;

    corpora: Corpus[];
    selectedCorpus: Corpus;

    categories: MethodCategory[];
    selectedCategory: MethodCategory;

    categories$: Observable<MethodCategory[]>;

    constructor(
        private router: Router,
        private corpusService: CorpusService,
        private uploadFileService: UploadFileService,
        private methodService: MethodService,
        private route: ActivatedRoute
    ) {}

    ngOnInit() {
        this.corpusService.list().subscribe((res) => {
            this.corpora = res;
        });

        this.corpusService
            .list()
            .pipe(
                switchMap((response: Corpus[]) => {
                    this.corpora = response;
                    return this.route.queryParams;
                })
            )
            .subscribe((params: Params) => {
                if (params.corpus) {
                    this.selectedCorpus = this.corpora.find(
                        (c) => c.id === +params.corpus
                    );
                    this.onSelectCorpus();
                }
            });

        this.categories$ = this.methodService.getCategories();
    }

    fullyFilled(): boolean {
        return (
            (this.newCorpusName || this.selectedCorpus) &&
            this.selectedCategory &&
            !this.corpusNameInUse() &&
            this.fileInput.files.length > 0
        );
    }

    onSelectCorpus(): void {
        if (this.selectedCorpus) {
            this.methodService
                .getCategory(this.selectedCorpus.method_category)
                .subscribe((next) => (this.selectedCategory = next));
            this.newCorpusName = undefined;
        } else {
            this.selectedCategory = undefined;
        }
    }

    corpusNameInUse(): boolean {
        return _.some(this.corpora, ['name', this.newCorpusName]);
    }

    createCorpus$(): Observable<Corpus> {
        const newCorpus: Corpus = {
            name: this.newCorpusName,
            status: 'created',
            method_category: this.selectedCategory.id,
        };
        return this.corpusService.create(newCorpus);
    }

    onUpload(event: FileUploadHandlerEvent): void {
        // Triggered by PrimeNG file upload component
        this.files = event.files;
    }

    upload$(toCorpus: Corpus, file: File): Observable<UploadFile> {
        const newUploadFile: UploadFile = {
            name: file.name,
            content: file,
            status: 'uploading',
            corpus: toCorpus,
        };
        return this.uploadFileService.upload(newUploadFile);
    }

    uploadFiles$(toCorpus: Corpus): Observable<UploadFile[]> {
        const uploadFiles: UploadFile[] = this.files.map((f: File) => ({
            name: f.name,
            content: f,
            status: 'uploading',
            corpus: toCorpus,
        }));
        return forkJoin(
            uploadFiles.map((file) => this.uploadFileService.upload(file))
        );
    }

    startUpload(): void {
        this.uploading = true;
        let uploadSteps$: Observable<UploadFile[]>;

        this.fileInput.upload();

        if (!this.selectedCorpus && this.newCorpusName) {
            uploadSteps$ = this.createCorpus$().pipe(
                concatMap((corpus) => this.uploadFiles$(corpus))
            );
        } else {
            uploadSteps$ = this.uploadFiles$(this.selectedCorpus);
        }

        uploadSteps$.subscribe(
            (response) => {
                this.uploading = false;
                this.router.navigate([`/process/${response[0].corpus}`]);
            },
            (error) => {
                console.error(error);
                this.uploading = false;
            }
        );
    }
}
