import { Component, Input } from '@angular/core';
import {
    faCheck,
    faExclamationTriangle,
    faQuestion,
    faMinus,
} from '@fortawesome/free-solid-svg-icons';

@Component({
    standalone: false,
    // eslint-disable-next-line @angular-eslint/component-selector
    selector: 'td[sas-transcript-progress-cell]',
    templateUrl: './transcript-progress-cell.component.html',
    styleUrls: ['./transcript-progress-cell.component.scss'],
})
export class TranscriptProgressCellComponent {
    @Input() evalProgress: () => number;
    faQuestion = faQuestion;
    faExclamation = faExclamationTriangle;
    faCheck = faCheck;
    faMinus = faMinus;

    constructor() {}
}
