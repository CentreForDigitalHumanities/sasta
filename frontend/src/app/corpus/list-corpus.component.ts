import { Component, OnDestroy, OnInit } from '@angular/core';
import { faPlus, faTrash } from '@fortawesome/free-solid-svg-icons';
import { ConfirmationService, MessageService } from 'primeng/api';
import { interval, Observable, Subscription } from 'rxjs';
import { startWith } from 'rxjs/operators';
import { Corpus } from '../models/corpus';
import { AuthService } from '../services/auth.service';
import { CorpusService } from '../services/corpus.service';

// check every 10 seconds
const UPDATE_INTERVAL = 10000;

@Component({
    selector: 'sas-list-corpus',
    templateUrl: './list-corpus.component.html',
    styleUrls: ['./list-corpus.component.scss'],
})
export class ListCorpusComponent implements OnInit, OnDestroy {
    interval$: Observable<number> = interval(UPDATE_INTERVAL);
    corpora$: Observable<Corpus[]>;
    faTrash = faTrash;
    faPlus = faPlus;

    private subscription$: Subscription;

    constructor(
        public corpusService: CorpusService,
        private confirmationService: ConfirmationService,
        private messageService: MessageService,
        public authService: AuthService
    ) {}

    ngOnDestroy() {
        this.subscription$.unsubscribe();
    }

    ngOnInit() {
        this.corpora$ = this.corpusService.getCorpora();
        this.subscription$ = this.interval$
            .pipe(startWith(0))
            .subscribe(() => this.refreshCorpora());
    }

    refreshCorpora(): void {
        this.corpusService.init();
    }

    confirmDeleteCorpus(event: Event, corpus: Corpus): void {
        event.stopImmediatePropagation();
        this.confirmationService.confirm({
            target: event.target,
            message: 'Are you sure you want to delete the corpus?',
            header: 'Confirm delete',
            acceptButtonStyleClass: 'button is-primary',
            rejectButtonStyleClass: 'button',
            accept: () => this.deleteCorpus(corpus),
        });
    }

    deleteCorpus(corpus: Corpus): void {
        this.corpusService.delete(corpus).subscribe(
            () => {
                this.messageService.add({
                    severity: 'success',
                    summary: `Corpus ${corpus.name} deleted`,
                });
                this.refreshCorpora();
            },
            () =>
                this.messageService.add({
                    severity: 'error',
                    summary: 'Corpus delete failed',
                })
        );
    }
}
