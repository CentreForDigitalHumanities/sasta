import { HttpClient, HttpResponse } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable } from 'rxjs';
import { map, switchMap, tap } from 'rxjs/operators';
import { User } from '@models';
import { environment } from '../../../environments/environment';

interface DetailResponse {
    detail: string;
}

type UserInfoResponse = Pick<User, 'username' | 'email'>;

@Injectable({
    providedIn: 'root',
})
export class AuthService {
    authAPI = '/rest-auth';
    isAuthenticated$ = new BehaviorSubject<boolean>(false);
    currentUser$ = new BehaviorSubject<User>(null);

    constructor(private httpClient: HttpClient) {
        this.setUser();
    }

    setUser(): void {
        this.getCompleteUser().subscribe(
            (userData) => {
                this.isAuthenticated$.next(true);
                this.currentUser$.next(userData);
            },
            () => {
                this.isAuthenticated$.next(false);
                this.currentUser$.next(null);
            },
        );
    }

    login(username: string, password: string): Observable<string> {
        return this.httpClient
            .post<string>(`${this.authAPI}/login/`, {
                username,
                password,
            })
            .pipe(tap(() => this.setUser()));
    }

    logout(): Observable<DetailResponse> {
        return this.httpClient
            .post<DetailResponse>(`${this.authAPI}/logout/`, {})
            .pipe(
                tap(() => {
                    this.currentUser$.next(null);
                    this.isAuthenticated$.next(false);
                }),
            );
    }

    register(
        username: string,
        password1: string,
        password2: string,
        email: string,
    ): Observable<DetailResponse> {
        return this.httpClient.post<DetailResponse>(
            `${this.authAPI}/registration/`,
            {
                username,
                password1,
                password2,
                email,
            },
        );
    }

    getCompleteUser(): Observable<User> {
        return this.httpClient.get<User>(`${this.authAPI}/user/`).pipe(
            switchMap((user) =>
                this.isAdmin().pipe(
                    map((adminStatus) => {
                        user.isAdmin = adminStatus;
                        return user;
                    }),
                ),
            ),
        );
    }

    isAdmin(): Observable<boolean> {
        return this.httpClient
            .get<{
                has_admin_access: boolean;
            }>(`${this.authAPI}/has_admin_access/`)
            .pipe(map((response) => response.has_admin_access as boolean));
    }

    infoFromConfirmKey(key: string): Observable<UserInfoResponse> {
        return this.httpClient.get<UserInfoResponse>(
            `${this.authAPI}/infofromkey/${key}/`,
        );
    }

    confirmEmail(key: string): Observable<DetailResponse> {
        return this.httpClient.post<DetailResponse>(
            `${this.authAPI}/registration/verify-email/`,
            { key },
        );
    }

    getDocumentation(): Observable<HttpResponse<unknown>> {
        return this.httpClient.get(environment.docs, { observe: 'response' });
    }

    requestResetPassword(email: string): Observable<{ detail: string }> {
        return this.httpClient.post<{ detail: string }>(
            `${this.authAPI}/password/reset/`,
            { email },
        );
    }

    public resetPassword(
        uid: string,
        token: string,
        newPassword1: string,
        newPassword2: string,
    ): Observable<{ detail: string }> {
        return this.httpClient.post<{ detail: string }>(
            `${this.authAPI}/password/reset/confirm/`,
            {
                uid,
                token,
                new_password1: newPassword1,
                new_password2: newPassword2,
            },
        );
    }
}
