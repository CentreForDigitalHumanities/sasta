import { Component, OnInit } from '@angular/core';
import { MethodService } from '@services';
import { Method } from '@models';
import { Observable } from 'rxjs';

@Component({
    standalone: false,
    selector: 'sas-list-method',
    templateUrl: './list-method.component.html',
    styleUrls: ['./list-method.component.scss'],
})
export class ListMethodComponent implements OnInit {
    methods$: Observable<Method[]>;

    constructor(private methodService: MethodService) {}

    ngOnInit() {
        this.methods$ = this.methodService.getMethods();
    }
}
