import { Component, OnInit } from '@angular/core';
import { HttpService } from '../http.service';

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.css']
})
export class RegisterComponent implements OnInit {
  message: string;
  username: string;
  password: string;

  constructor(private httpService: HttpService) { }

  ngOnInit() {
  }

  register(){
    this.httpService.register(this.username, this.password).subscribe(
      message => {
        this.message = message.username;
      },
      error => {
        console.log(error.status);
        this.message = 'Unable to register';
      }
    );
  }
}
