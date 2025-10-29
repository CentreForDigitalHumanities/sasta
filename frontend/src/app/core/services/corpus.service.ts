import { HttpClient, HttpResponse } from '@angular/common/http';
import { DestroyRef, inject, Injectable } from '@angular/core';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { Corpus, ListedCorpus } from '@models';
import { Observable, Subject } from 'rxjs';

@Injectable({
    providedIn: 'root',
})
export class CorpusService {
    readonly #destroyRef = inject(DestroyRef);

    private corpora$: Subject<ListedCorpus[]> = new Subject();

    constructor(private httpClient: HttpClient) {}

    public getCorpora(): Observable<ListedCorpus[]> {
        return this.corpora$;
    }

    public refresh(): void {
        this.httpClient
            .get<ListedCorpus[]>('/api/corpora/')
            .pipe(takeUntilDestroyed(this.#destroyRef))
            .subscribe((corpora) => this.corpora$.next(corpora));
    }

    create(corpus: Corpus): Observable<Corpus> {
        return this.httpClient.post<Corpus>('/api/corpora/', corpus);
    }

    delete(corpus: Corpus | ListedCorpus): Observable<null> {
        return this.httpClient.delete<null>(`/api/corpora/${corpus.id}/`);
    }

    list(): Observable<ListedCorpus[]> {
        return this.httpClient.get<ListedCorpus[]>('/api/corpora/');
    }

    getByID(id: number): Observable<Corpus> {
        return this.httpClient.get<Corpus>(`/api/corpora/${id}/`);
    }

    convertAll(id: number): Observable<Corpus> {
        return this.httpClient.get<Corpus>(`/api/corpora/${id}/convert_all/`);
    }

    parseAll(id: number): Observable<Corpus> {
        return this.httpClient.get<Corpus>(`/api/corpora/${id}/parse_all/`);
    }

    parseAllAsync(id: number): Observable<string> {
        // returns task id
        return this.httpClient.get<string>(
            `/api/corpora/${id}/parse_all_async/`
        );
    }

    downloadZip(id: number): Observable<HttpResponse<Blob>> {
        const formData: FormData = new FormData();
        return this.httpClient.post(`/api/corpora/${id}/download/`, formData, {
            observe: 'response',
            responseType: 'blob',
        });
    }

    setDefaultMethod(
        id: number,
        methodID: string | Blob
    ): Observable<'Success'> {
        const formData: FormData = new FormData();
        formData.append('method', methodID);
        return this.httpClient.post<'Success'>(
            `/api/corpora/${id}/defaultmethod/`,
            formData
        );
    }
}
