import { HttpErrorResponse } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { NgForm } from '@angular/forms';
import { Title } from '@angular/platform-browser';
import { AuthService } from '@services';
import * as _ from 'lodash';
import { faEnvelope } from '@fortawesome/free-solid-svg-icons';

@Component({
    selector: 'sas-request-reset',
    templateUrl: './request-reset.component.html',
    styleUrls: ['./request-reset.component.scss'],
})
export class RequestResetComponent implements OnInit {
    public email: string;
    public success: boolean;
    public showMessage: boolean;
    public message: string;

    appName = 'SASTA';
    faEnvelope = faEnvelope;

    constructor(
        private authService: AuthService,
        private title: Title
    ) {}

    ngOnInit() {
        this.title.setTitle('Reset password');
    }

    requestReset(requestResetForm: NgForm): void {
        const email: string = requestResetForm.value.email;
        this.authService.requestResetPassword(email).subscribe(
            (res) => this.handleSuccess(res),
            (err) => this.handleError(err)
        );
    }

    disableNotification(): void {
        this.showMessage = false;
    }

    handleSuccess(response: {detail: string}): void {
        this.success = true;
        this.message = response.detail;
        this.showMessage = true;
    }

    handleError(response: HttpErrorResponse): void {
        this.success = false;
        this.message = _.join(_.values(response.error), ',');
        this.showMessage = true;
    }
}
