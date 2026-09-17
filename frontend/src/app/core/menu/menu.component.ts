import { Component, NgZone, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { environment } from '@envs/environment';
import {
    faExternalLinkAlt,
    faFileUpload,
    faFolder,
    faHome,
    faListAlt,
    faUser,
    faUserShield,
} from '@fortawesome/free-solid-svg-icons';
import { AuthService } from '@services';
import { ShowState, animations } from '@shared/animations';

@Component({
    standalone: false,
    animations,
    selector: 'sas-menu',
    templateUrl: './menu.component.html',
    styleUrls: ['./menu.component.scss'],
})
export class MenuComponent implements OnInit {
    burgerShow: ShowState;
    burgerActive = false;

    faUser = faUser;
    faFolder = faFolder;
    faListAlt = faListAlt;
    faFileUpload = faFileUpload;
    faUserShield = faUserShield;
    faExternalLink = faExternalLinkAlt;
    faHome = faHome;

    version = environment.appVersion;
    docsAvailable: boolean;

    constructor(
        private ngZone: NgZone,
        public authService: AuthService,
        private router: Router
    ) {}

    ngOnInit(): void {
        this.authService.getDocumentation().subscribe(
            (res) => (this.docsAvailable = res.status === 200),
            (err) => (this.docsAvailable = err.status === 200)
        );
    }

    isAuthenticated(): boolean {
        return this.authService.isAuthenticated$.getValue();
    }

    logout(): void {
        this.authService.logout().subscribe(
            () => {
                this.router.navigate(['/login']);
            },
            (err) => console.error('Http Error', err)
        );
    }

    toggleBurger(): void {
        if (!this.burgerActive) {
            // make it active to make it visible (add a class to
            // override it being hidden for smaller screens)
            this.burgerActive = true;
            // immediately hide it
            this.burgerShow = 'hide';
            setTimeout(() => {
                this.ngZone.run(() => {
                    // trigger the transition
                    this.burgerShow = 'show';
                });
            });
            return;
        }

        this.burgerShow = this.burgerShow === 'show' ? 'hide' : 'show';
    }

    navigateToDocs(): void {
        window.open(environment.docs, '_blank');
    }
}
