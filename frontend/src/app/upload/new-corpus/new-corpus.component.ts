import { HttpErrorResponse } from '@angular/common/http';
import { Component, DestroyRef, inject, OnInit, Output } from '@angular/core';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { CorpusService, MethodService } from '@services';
import { Corpus, MethodCategory } from '@shared/models';
import { BehaviorSubject, Observable, Subject } from 'rxjs';
import { finalize, tap } from 'rxjs/operators';

@Component({
    selector: 'sas-new-corpus',
    templateUrl: './new-corpus.component.html',
    styleUrls: ['./new-corpus.component.scss'],
})
export class NewCorpusComponent implements OnInit {
    readonly #destroyRef = inject(DestroyRef);

    loading$ = new BehaviorSubject<boolean>(false);
    errors$ = new Subject<'notUnique'>();

    categories$: Observable<MethodCategory[]>;
    selectedCategory: MethodCategory;
    newCorpus: Corpus = {
        name: '',
        method_category: null,
        share_permission: false,
    };

    @Output() accept = new Subject<Corpus>();
    @Output() cancel = new Subject<void>();

    constructor(
        private corpusService: CorpusService,
        private methodService: MethodService
    ) {}

    ngOnInit(): void {
        this.categories$ = this.methodService
            .getCategories()
            .pipe(takeUntilDestroyed(this.#destroyRef));
    }

    onSubmit(): void {
        this.corpusService
            .create(this.newCorpus)
            .pipe(
                tap(() => this.loading$.next(true)),
                takeUntilDestroyed(this.#destroyRef),
                finalize(() => this.loading$.next(false))
            )
            .subscribe({
                next: this.handleSuccess.bind(this),
                error: this.handleFailure.bind(this),
            });
    }

    handleSuccess(corpus: Corpus): void {
        this.accept.next(corpus);
    }

    handleFailure(errors: HttpErrorResponse): void {
        if (
            errors.error &&
            errors.error.detail ===
                'Corpus with unique constraints already exists.'
        ) {
            this.errors$.next('notUnique');
        } else {
            console.error(errors);
        }
    }
}
