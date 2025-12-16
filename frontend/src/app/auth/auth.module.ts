import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { LoginComponent } from './login.component';
import { RegisterComponent } from './register.component';
import { VerifyComponent } from './verify.component';
import { SharedModule } from '../shared/shared.module';
import { RequestResetComponent } from './reset-password/request-reset.component';
import { ResetPasswordComponent } from './reset-password//reset-password.component';

@NgModule({
    declarations: [
        LoginComponent,
        RegisterComponent,
        VerifyComponent,
        RequestResetComponent,
        ResetPasswordComponent,
    ],
    imports: [CommonModule, SharedModule],
    exports: [LoginComponent, RegisterComponent, VerifyComponent],
})
export class AuthModule {}
