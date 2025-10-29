import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { UploadFile } from '@models';
import { Observable } from 'rxjs';

@Injectable({
    providedIn: 'root',
})
export class UploadFileService {
    constructor(private httpClient: HttpClient) {}

    upload(uploadFile: UploadFile): Observable<UploadFile> {
        const formData: FormData = new FormData();
        formData.append(
            'content',
            uploadFile.content as File,
            uploadFile.content.name
        );
        formData.append('name', uploadFile.name);
        formData.append('corpus', String(uploadFile.corpus_id));
        formData.append('status', 'pending');
        return this.httpClient.post<UploadFile>('/api/upload_files/', formData);
    }
}
