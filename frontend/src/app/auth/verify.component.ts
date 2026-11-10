import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { MessageService } from 'primeng/api';
import { AuthService } from '@services';

@Component({
    standalone: false,
    selector: 'sas-verify',
    templateUrl: './verify.component.html',
    styleUrls: ['./verify.component.scss'],
})
export class VerifyComponent implements OnInit {
    key: string;
    username: string;
    email: string;

    constructor(
        private route: ActivatedRoute,
        private authService: AuthService,
        private messageService: MessageService,
        private router: Router
    ) {
        this.route.paramMap.subscribe(
            (params) => (this.key = params.get('key'))
        );
    }

    ngOnInit() {
        this.authService.infoFromConfirmKey(this.key).subscribe((res) => {
            this.username = res.username;
            this.email = res.email;
        });
    }

    confirm(): void {
        this.authService.confirmEmail(this.key).subscribe(
            () => {
                this.messageService.add({
                    severity: 'success',
                    summary: 'E-mail address confirmed',
                    detail: '',
                });
                this.authService.logout().subscribe();
                this.router.navigate(['/login']);
            },
            () => {
                this.messageService.add({
                    severity: 'error',
                    summary: 'Cannot confirm email-address',
                    detail: '',
                });
            }
        );
    }
}
