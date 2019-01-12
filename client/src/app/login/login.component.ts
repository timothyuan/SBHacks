import { Component, OnInit } from '@angular/core';
import { HttpService } from '../http.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {
  message: string;
  username: string;
  password: string;

  constructor(private httpService: HttpService, private router: Router) { }

  ngOnInit() {
  }

  login(){
    this.httpService.login(this.username, this.password).subscribe(
      message => {
        console.log(message.id);
        this.router.navigate(['../user', this.username, message.id]);
      },
      error => {
        console.log(error.status);
        this.message = 'Unable to login';
      }
    );
  }
}
