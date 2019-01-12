import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable} from 'rxjs';

const httpOptions = {
  headers: new HttpHeaders({ 'Content-Type': 'application/json' })
};

@Injectable({
  providedIn: 'root'
})
export class HttpService {

  constructor(private http: HttpClient) { }

  login(username: string, password: string): Observable<any> {
    let data = {
      username: username,
      password: password
    }
    return this.http.post<string>(window.location.origin + '/user/login', data, httpOptions);
  }

  register(username: string, password: string): Observable<any> {
    let data = {
      username: username,
      password: password
    }
    return this.http.post<string>(window.location.origin + '/user/register', data, httpOptions);
  }

  upload(username: string, id: string, file: File): Observable<any> {
    let uploadData = new FormData();
    uploadData.append('username', username);
    uploadData.append('id', id);
    uploadData.append('file', file);
    return this.http.post<string>(window.location.origin + '/user/upload', uploadData);
  }

  images(id: string): Observable<any>{
    let data = {
      id: id
    }
    return this.http.post<string[]>(window.location.origin + '/user/images', data);
  }
}
