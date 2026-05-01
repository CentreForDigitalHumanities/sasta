import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import _ from 'lodash';
import { BehaviorSubject, Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import { Method } from '@models';
import { MethodCategory } from '@models';
import { SelectItemGroup } from 'primeng/api';

@Injectable({
    providedIn: 'root',
})
export class MethodService {
    private methods$ = new BehaviorSubject<Method[]>([]);
    private categories$ = new BehaviorSubject<MethodCategory[]>([]);

    constructor(private http: HttpClient) {
        this.initCategories();
        this.initMethods();
    }

    public initCategories(): void {
        this.http
            .get<MethodCategory[]>('/api/method_categories/')
            .subscribe((categories) => this.categories$.next(categories));
    }

    public initMethods(): void {
        this.http
            .get<Method[]>('/api/assessment_methods/')
            .subscribe((methods) => this.methods$.next(methods));
    }

    public getMethods(): Observable<Method[]> {
        return this.methods$;
    }

    public getMethodsForCategory(c: MethodCategory): Observable<Method[]> {
        return this.methods$.pipe(
            map((methods) =>
                methods.filter((method) => method.category.id === c.id)
            )
        );
    }

    public getCategories(): Observable<MethodCategory[]> {
        return this.categories$;
    }

    public getCategory(id: number): Observable<MethodCategory> {
        return this.categories$.pipe(
            map((cats) => cats.filter((cat) => cat.id === id)),
            map((cats) => cats[0])
        );
    }

    public getMethod(id: number): Observable<Method> {
        return this.methods$.pipe(
            map((methods) => methods.filter((method) => method.id === id)),
            map((methods) => methods[0])
        );
    }

    async upload(method: Method): Promise<Method> {
        const formData: FormData = new FormData();
        formData.append('content', method.content as File, method.content.name);
        formData.append('name', method.name);
        const response = await this.http
            .post<Method>('/api/assessment_methods/', formData)
            .toPromise();
        return response;
    }

    groupMethods(methods: Method[], categoryID: number): SelectItemGroup[] {
        return _(methods)
            .filter(
                (m: { category: { id: number } }) =>
                    m.category.id === categoryID
            )
            .groupBy('category.name')
            .map((groupedMethods, methodCat: string) => ({
                label: methodCat,
                items: _.map(groupedMethods, (m: Method) => ({
                    label: m.name,
                    value: m,
                })),
            }))
            .value();
    }
}
