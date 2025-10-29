import { ComponentFixture, TestBed } from '@angular/core/testing';

import { NewCorpusComponent } from './new-corpus.component';

describe('NewCorpusComponent', () => {
    let component: NewCorpusComponent;
    let fixture: ComponentFixture<NewCorpusComponent>;

    beforeEach(() => {
        TestBed.configureTestingModule({
            declarations: [NewCorpusComponent],
        });
        fixture = TestBed.createComponent(NewCorpusComponent);
        component = fixture.componentInstance;
        fixture.detectChanges();
    });

    it('should create', () => {
        expect(component).toBeTruthy();
    });
});
