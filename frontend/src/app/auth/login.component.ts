import { HttpErrorResponse } from '@angular/common/http';
import { Component, OnDestroy } from '@angular/core';
import { Router } from '@angular/router';
import { faLock, faUser } from '@fortawesome/free-solid-svg-icons';
import { AuthService } from '@services';
import * as _ from 'lodash';
import { Subject } from 'rxjs';
import { takeUntil } from 'rxjs/operators';

@Component({
    selector: 'sas-login',
    templateUrl: './login.component.html',
    styleUrls: ['./login.component.scss'],
})
export class LoginComponent implements OnDestroy {
    faLock = faLock;
    faUser = faUser;

    username: string;
    password: string;

    processing = false;

    messages: { severity: string; summary: string; detail: string }[] = [];

    onDestroy$: Subject<void> = new Subject<void>();

    errors$ = new Subject<string[]>();

    constructor(private authService: AuthService, private router: Router) {}

    ngOnDestroy() {
        this.onDestroy$.next();
    }

    login(): void {
        this.processing = true;
        this.messages = [];
        this.authService
            .login(this.username, this.password)
            .pipe(takeUntil(this.onDestroy$))
            .subscribe(this.handleSuccess, this.handleError);
    }

    handleSuccess = (): void => {
        this.processing = false;
        this.router.navigate(['']);
    };

    handleError = (errorResponse: HttpErrorResponse): void => {
        this.processing = false;
        if (errorResponse && errorResponse.status === 400) {
            this.errors$.next(_.flatten(_.values(errorResponse.error)));
        } else {
            this.errors$.next([
                'Unknown error logging in. If this problem persists, please contact the developers.',
            ]);
        }
    };
}
