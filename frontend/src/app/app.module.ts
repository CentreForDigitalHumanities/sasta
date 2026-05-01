import { HttpClientModule, HttpClientXsrfModule } from '@angular/common/http';
import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { BrowserModule } from '@angular/platform-browser';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { XmlParseService } from '@services';
import { LassyXPathModule } from 'lassy-xpath';
import { ConfirmationService, MessageService } from 'primeng/api';
import { providePrimeNG } from 'primeng/config';
import Lara from '@primeng/themes/lara';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { AuthModule } from './auth/auth.module';
import { CoreModule } from './core/core.module';
import { CorpusModule } from './corpus/corpus.module';
import { ProcessComponent } from './process/process.component';
import { TranscriptProgressCellComponent } from './process/transcript-progress-cell.component';
import { TranscriptProgressComponent } from './process/transcript-progress.component';
import { SharedModule } from './shared/shared.module';
import { TranscriptComponent } from './transcript/transcript.component';
import { UploadSafComponent } from './transcript/upload-saf.component';
import { TreeVisualizerComponent } from './tree-visualizer/tree-visualizer.component';
import { UploadModule } from './upload/upload.module';
import { UtterancesListComponent } from './utterances/utterances-list.component';
import { APP_BASE_HREF } from '@angular/common';

@NgModule({
    declarations: [
        AppComponent,
        ProcessComponent,
        TranscriptComponent,
        UploadSafComponent,
        TranscriptProgressComponent,
        TranscriptProgressCellComponent,
        UtterancesListComponent,
        TreeVisualizerComponent,
    ],
    imports: [
        AppRoutingModule,
        BrowserModule,
        BrowserAnimationsModule,
        FormsModule,
        HttpClientModule,
        HttpClientXsrfModule.withOptions({
            cookieName: 'csrftoken',
            headerName: 'X-CSRFToken',
        }),
        LassyXPathModule,
        // Shared and core modules
        CoreModule,
        SharedModule,
        // Feature modules
        AuthModule,
        CorpusModule,
        UploadModule,
    ],
    providers: [
        ConfirmationService,
        MessageService,
        XmlParseService,
        { provide: APP_BASE_HREF, useValue: '/' },
        providePrimeNG({ theme: { preset: Lara } }),
    ],
    bootstrap: [AppComponent],
})
export class AppModule {}
