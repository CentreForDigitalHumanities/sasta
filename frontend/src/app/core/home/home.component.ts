import { Component } from '@angular/core';
import { SafeResourceUrl } from '@angular/platform-browser';
import { AuthService } from '../services/auth.service';
import { environment } from '@envs/environment';

@Component({
    standalone: false,
    selector: 'sas-home',
    templateUrl: './home.component.html',
    styleUrls: ['./home.component.scss'],
})
export class HomeComponent {
    isAuthenticated$ = this.authService.isAuthenticated$;
    aboutUrl: SafeResourceUrl;

    constructor(private authService: AuthService) {}

    navigateToDocs(): void {
        window.open(environment.docs, '_blank');
    }
}
