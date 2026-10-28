import { Component } from '@angular/core';
import { environment } from '@envs/environment';

@Component({
    selector: 'sas-footer',
    templateUrl: './footer.component.html',
    styleUrls: ['./footer.component.scss'],
})
export class FooterComponent {
    privacyUrl = `${environment.docs}/privacy/`;

    constructor() {}
}
