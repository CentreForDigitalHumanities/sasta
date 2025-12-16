import { ComponentFixture, TestBed } from '@angular/core/testing';

import { RequestResetComponent } from './request-reset.component';
import { HttpClientTestingModule } from '@angular/common/http/testing';
import { RouterTestingModule } from '@angular/router/testing';
import { FormsModule } from '@angular/forms';

describe('RequestResetComponent', () => {
    let component: RequestResetComponent;
    let fixture: ComponentFixture<RequestResetComponent>;

    beforeEach(() => {
        TestBed.configureTestingModule({
            declarations: [RequestResetComponent],
            imports: [
                HttpClientTestingModule,
                RouterTestingModule,
                FormsModule,
            ],
        });
        fixture = TestBed.createComponent(RequestResetComponent);
        component = fixture.componentInstance;
        fixture.detectChanges();
    });

    it('should create', () => {
        expect(component).toBeTruthy();
    });
});
