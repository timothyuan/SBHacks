import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { map }                from 'rxjs/operators';
import { NgbModal } from '@ng-bootstrap/ng-bootstrap';
import { HttpService } from '../http.service';
import { UploadModalComponent } from '../upload-modal/upload-modal.component';

@Component({
  selector: 'app-user',
  templateUrl: './user.component.html',
  styleUrls: ['./user.component.css']
})
export class UserComponent implements OnInit {
  username: string;
  id: string;
  images: string[];

  constructor(private route: ActivatedRoute, private modalService: NgbModal, private httpService: HttpService) { }

  ngOnInit() {
    this.getParams();
    this.getImages();
  }

  getParams(){
    this.username = this.route.snapshot.paramMap.get('username');
    this.id = this.route.snapshot.paramMap.get('id');
  }

  getImages(){
    this.httpService.images(this.id).subscribe(
      result => {
        this.images = result.images;
      },
      error => {
        console.log(error.status);
      }
    );
  }

  openUploadModal() {
    const modalRef = this.modalService.open(UploadModalComponent);
    modalRef.componentInstance.username = this.username;
    modalRef.componentInstance.id = this.id;
  }

}
