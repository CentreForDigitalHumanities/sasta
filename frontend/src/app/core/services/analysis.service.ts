import { HttpClient, HttpResponse } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { TaskResult } from '@shared/models';
import { Observable, timer } from 'rxjs';
import { filter, switchMap, take, tap } from 'rxjs/operators';

export type AnnotationOutputFormat = 'xlsx' | 'cha' | 'form';

@Injectable({
    providedIn: 'root',
})
export class AnalysisService {
    constructor(private http: HttpClient) {}

    query(
        transcriptID: number,
        methodID: string | Blob,
    ): Observable<HttpResponse<Blob>> {
        const formData: FormData = new FormData();
        formData.append('method', methodID);
        return this.http.post(
            `/api/transcripts/${transcriptID}/query/`,
            formData,
            { observe: 'response', responseType: 'blob' },
        );
    }

    annotate(
        transcriptID: number,
        methodID: string | Blob,
        outputFormat: AnnotationOutputFormat,
    ): Observable<HttpResponse<Blob>> {
        const formData: FormData = new FormData();
        formData.append('method', methodID);
        formData.append('format', outputFormat);
        return this.http.post(
            `/api/transcripts/${transcriptID}/annotate/`,
            formData,
            { observe: 'response', responseType: 'blob' },
        );
    }

    generateForm(
        transcriptID: number,
        methodID: string | Blob,
    ): Observable<HttpResponse<Blob>> {
        const formData: FormData = new FormData();
        formData.append('method', methodID);
        return this.http.post(
            `/api/transcripts/${transcriptID}/generateform/`,
            formData,
            { observe: 'response', responseType: 'blob' },
        );
    }

    // async analysis
    taskSuccess = (response: TaskResult): boolean =>
        response.status === 'SUCCESS';

    createAnalysisTask(
        transcriptID: number,
        methodID: string,
    ): Observable<string> {
        const data: FormData = new FormData();
        data.append('method', methodID);
        return this.http.post<string>(
            `/api/transcripts/${transcriptID}/analyse_async/`,
            data,
        );
    }

    getAnalysisTask(taskID: string): Observable<TaskResult> {
        return this.http.get<TaskResult>(`/api/analysis/tasks/${taskID}/`);
    }

    pollAnalysisTask(taskID: string): Observable<TaskResult> {
        return timer(0, 1000).pipe(
            switchMap((_) => this.getAnalysisTask(taskID)),
            filter(this.taskSuccess),
            take(1),
        );
    }

    getResults(
        transcriptID: number,
        format: 'xlsx' | 'cha' | 'form',
    ): Observable<HttpResponse<Blob>> {
        const formData: FormData = new FormData();
        formData.append('format', format);
        return this.http.post(
            `/api/transcripts/${transcriptID}/results/`,
            formData,
            { observe: 'response', responseType: 'blob' },
        );
    }
}
