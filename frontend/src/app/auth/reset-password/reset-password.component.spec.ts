import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ResetPasswordComponent } from './reset-password.component';
import { HttpClientTestingModule } from '@angular/common/http/testing';
import { RouterTestingModule } from '@angular/router/testing';
import { FormsModule } from '@angular/forms';

describe('ResetPasswordComponent', () => {
    let component: ResetPasswordComponent;
    let fixture: ComponentFixture<ResetPasswordComponent>;

    beforeEach(() => {
        TestBed.configureTestingModule({
            declarations: [ResetPasswordComponent],
            imports: [
                HttpClientTestingModule,
                RouterTestingModule,
                FormsModule,
            ],
        });
        fixture = TestBed.createComponent(ResetPasswordComponent);
        component = fixture.componentInstance;
        fixture.detectChanges();
    });

    it('should create', () => {
        expect(component).toBeTruthy();
    });
});
