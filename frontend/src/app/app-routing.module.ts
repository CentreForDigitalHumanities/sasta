import { NgModule } from '@angular/core';
import { RouterModule } from '@angular/router';
import { AuthGuard } from './auth/auth.guard';
import { Routes } from '@angular/router';
import { LoginComponent } from './auth/login.component';
import { RegisterComponent } from './auth/register.component';
import { VerifyComponent } from './auth/verify.component';
import { TranscriptComponent } from './transcript/transcript.component';
import { ProcessComponent } from './process/process.component';
import { UploadComponent } from './upload/upload.component';
import { HomeComponent } from './core/home/home.component';
import { RequestResetComponent } from './auth/reset-password/request-reset.component';
import { ResetPasswordComponent } from './auth/reset-password/reset-password.component';

const routes: Routes = [
    {
        path: 'corpora',
        loadChildren: () =>
            import('./corpus/corpus.module').then((m) => m.CorpusModule),
    },
    {
        path: 'methods',
        loadChildren: () =>
            import('./method/method.module').then((m) => m.MethodModule),
    },
    {
        path: 'upload',
        component: UploadComponent,
        canActivate: [AuthGuard],
    },
    {
        path: 'transcript/:id',
        component: TranscriptComponent,
        canActivate: [AuthGuard],
    },
    {
        path: 'process/:id',
        component: ProcessComponent,
        canActivate: [AuthGuard],
    },
    {
        path: 'login',
        component: LoginComponent,
    },
    {
        path: 'register',
        component: RegisterComponent,
    },
    {
        path: 'confirm-email/:key',
        component: VerifyComponent,
    },
    {
        path: 'reset',
        component: RequestResetComponent,
    },
    {
        path: 'reset-password/:uid/:token',
        component: ResetPasswordComponent,
    },
    {
        path: '',
        component: HomeComponent,
    },
];

@NgModule({
    imports: [
        RouterModule.forRoot(routes, {}),
        RouterModule,
    ],
    exports: [RouterModule],
    providers: [AuthGuard],
    declarations: [],
})
export class AppRoutingModule {}
