import { HttpClientTestingModule } from '@angular/common/http/testing';
import { ComponentFixture, TestBed, waitForAsync } from '@angular/core/testing';
import { Transcript } from '@models';
import { MessageService } from 'primeng/api';

import { FontAwesomeTestingModule } from '@fortawesome/angular-fontawesome/testing';
import { UploadSafComponent } from './upload-saf.component';
import { DialogModule } from 'primeng/dialog';

describe('UploadSafComponent', () => {
    let component: UploadSafComponent;
    let fixture: ComponentFixture<UploadSafComponent>;

    const mockTranscript: Transcript = {
        id: 99,
        name: 'Tarsp_01',
        content: 'some/path/1.cha',
        parsed_content: 'some/path/1.xml',
        corrected_content: 'some/corrected/1.xml',
        status: 6,
        status_name: 'parsed',
        date_added: new Date(2021, 6, 3),
        corpus: 1,
        utterances: [
            {
                id: 1,
                for_analysis: true,
                sentence: 'hee',
                parse_tree: '',
                speaker: 'CHI',
                uttno: 1,
            },
            {
                id: 2,
                for_analysis: true,
                sentence: 'joe',
                parse_tree: '',
                speaker: 'INV',
                uttno: 2,
            },
        ],
    };

    beforeEach(waitForAsync(() => {
        TestBed.configureTestingModule({
            declarations: [UploadSafComponent],
            imports: [
                HttpClientTestingModule,
                FontAwesomeTestingModule,
                DialogModule,
            ],
            providers: [MessageService],
        }).compileComponents();
    }));

    beforeEach(() => {
        fixture = TestBed.createComponent(UploadSafComponent);
        component = fixture.componentInstance;
        component.transcript = mockTranscript;
        fixture.detectChanges();
    });

    it('should create', () => {
        expect(component).toBeTruthy();
    });
});
