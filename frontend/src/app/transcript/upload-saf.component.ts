import { HttpErrorResponse } from '@angular/common/http';
import {
    Component,
    EventEmitter,
    Input,
    OnDestroy,
    Output,
} from '@angular/core';
import { faUpload } from '@fortawesome/free-solid-svg-icons';
import { Transcript } from '@models';
import { AnnotationsService } from '@services';
import { MessageService } from 'primeng/api';

@Component({
    selector: 'sas-upload-saf',
    templateUrl: './upload-saf.component.html',
    styleUrls: ['./upload-saf.component.scss'],
})
export class UploadSafComponent implements OnDestroy {
    @Input() transcript: Transcript;
    @Input() display: boolean;

    @Output() displayChange = new EventEmitter();
    @Output() annotationsUploaded = new EventEmitter<void>();

    content: File;
    fileName: string;
    uploading: boolean;
    faUpload = faUpload;

    parseErrors: string[];

    constructor(
        private messageService: MessageService,
        private annotationsService: AnnotationsService,
    ) {}

    ngOnDestroy() {
        this.displayChange.unsubscribe();
    }

    onClose(): void {
        this.parseErrors = null;
        this.displayChange.emit(false);
    }

    header(): string {
        return `Upload corrections for ${this.transcript.name}`;
    }

    onFileChange(fileInput: HTMLInputElement): void {
        this.parseErrors = null;
        this.content = fileInput.files[0];
        this.fileName = this.content.name;
    }

    upload(): void {
        this.parseErrors = null;
        this.uploading = true;
        this.annotationsService
            .upload(this.fileName, this.content, this.transcript)
            .subscribe(
                () => {
                    this.uploading = false;
                    this.onClose();
                    this.annotationsUploaded.emit();
                    this.messageService.add({
                        severity: 'success',
                        summary: `Annotations uploaded for ${this.transcript.name}`,
                    });
                },
                (error) => this.handleErrors(error),
            );
    }

    handleErrors(httpError: HttpErrorResponse): void {
        this.uploading = false;
        if (Array.isArray(httpError.error)) {
            this.parseErrors = httpError.error;
        } else {
            this.parseErrors = [httpError.error];
        }
    }
}
