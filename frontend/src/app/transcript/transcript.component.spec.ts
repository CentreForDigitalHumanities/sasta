
import { HttpClientTestingModule } from '@angular/common/http/testing';
import { NO_ERRORS_SCHEMA } from '@angular/core';
import { ComponentFixture, TestBed, waitForAsync } from '@angular/core/testing';
import { RouterTestingModule } from '@angular/router/testing';
import { MessageService } from 'primeng/api';
import { SelectModule } from 'primeng/select';

import { TranscriptComponent } from './transcript.component';

describe('TranscriptComponent', () => {
    let component: TranscriptComponent;
    let fixture: ComponentFixture<TranscriptComponent>;

    beforeEach(waitForAsync(() => {
        TestBed.configureTestingModule({
            declarations: [TranscriptComponent],
            imports: [
                RouterTestingModule,
                HttpClientTestingModule,
                SelectModule,
            ],
            providers: [MessageService],
            schemas: [NO_ERRORS_SCHEMA],
        }).compileComponents();
    }));

    beforeEach(() => {
        fixture = TestBed.createComponent(TranscriptComponent);
        component = fixture.componentInstance;
        fixture.detectChanges();
    });

    it('should create', () => {
        expect(component).toBeTruthy();
    });
});
