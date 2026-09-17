import { Component, OnDestroy } from '@angular/core';
import { faLock, faUser, faEnvelope } from '@fortawesome/free-solid-svg-icons';
import { AuthService } from '@services';
import { Router } from '@angular/router';
import { MessageService } from 'primeng/api';
import { Subject } from 'rxjs';
import { takeUntil } from 'rxjs/operators';
import { HttpErrorResponse } from '@angular/common/http';

@Component({
    standalone: false,
    selector: 'sas-register',
    templateUrl: './register.component.html',
    styleUrls: ['./register.component.scss'],
})
export class RegisterComponent implements OnDestroy {
    faLock = faLock;
    faUser = faUser;
    faEnvelope = faEnvelope;

    username: string;
    emailAddress: string;
    password1 = '';
    password2: string;

    processing = false;

    onDestroy$: Subject<void> = new Subject<void>();

    constructor(
        private authService: AuthService,
        private router: Router,
        private messageService: MessageService
    ) {}

    ngOnDestroy() {
        this.onDestroy$.next();
    }

    passwordSame(): boolean {
        return (
            this.password1 &&
            this.password2 &&
            this.password1 === this.password2
        );
    }

    passwordMinLength(): boolean {
        return this.password1.length >= 8;
    }

    containsSpace(str: string): boolean {
        return str.indexOf(' ') >= 0;
    }

    usernameValid(): boolean {
        return !this.containsSpace(this.username);
    }

    onError(err: HttpErrorResponse): void {
        this.authService.isAuthenticated$.next(false);
        this.processing = false;
        let detailMsg;

        if (err.error.username) {
            detailMsg = err.error.username[0];
        } else if (err.error.email) {
            detailMsg = err.error.email[0];
        } else if (err.error.password1) {
            detailMsg = err.error.password1[0];
        } else {
            detailMsg = err.error;
        }
        const msg = {
            severity: 'error',
            summary: 'Registration failed.',
            detail: detailMsg,
            sticky: true,
        };
        this.messageService.add(msg);
    }

    register(): void {
        this.processing = true;
        this.authService
            .register(
                this.username,
                this.password1,
                this.password2,
                this.emailAddress
            )
            .pipe(takeUntil(this.onDestroy$))
            .subscribe(
                () => {
                    this.messageService.add({
                        severity: 'success',
                        summary: 'Registration success',
                        detail: `E-mail confirmation request sent to ${this.emailAddress}.`,
                        life: 6000,
                    });
                    this.router.navigate(['/login']);
                },
                (err) => {
                    this.onError(err);
                }
            );
    }
}
