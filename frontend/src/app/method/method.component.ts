import { Component, OnInit } from '@angular/core';
import { MethodService } from '@services';
import { ActivatedRoute } from '@angular/router';
import { Method, Query } from '@models';
import { faCheck, faSearch } from '@fortawesome/free-solid-svg-icons';

import * as _ from 'lodash';
import { Observable } from 'rxjs';

@Component({
    selector: 'sas-method',
    templateUrl: './method.component.html',
    styleUrls: ['./method.component.scss'],
})
export class MethodComponent implements OnInit {
    id: number;
    method$: Observable<Method>;
    selectedQuery: any;
    showDialog = false;
    _: any = _; // Lodash

    faCheck = faCheck;
    faSearch = faSearch;
    constructor(
        private methodService: MethodService,
        private route: ActivatedRoute
    ) {
        this.route.paramMap.subscribe(
            (params) => (this.id = +params.get('id'))
        );
    }

    ngOnInit() {
        this.method$ = this.methodService.getMethod(this.id);
    }

    showQuery(query: Query): void {
        this.selectedQuery = query;
        this.showDialog = true;
    }
}
