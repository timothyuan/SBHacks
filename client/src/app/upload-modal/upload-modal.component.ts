import { Component, OnInit, Input } from '@angular/core';
import { NgbActiveModal } from '@ng-bootstrap/ng-bootstrap';
import { HttpService } from '../http.service';

@Component({
  selector: 'app-upload-modal',
  templateUrl: './upload-modal.component.html',
  styleUrls: ['./upload-modal.component.css']
})
export class UploadModalComponent implements OnInit {

  @Input() username: string;
  @Input() id: string;
  private fileToUpload: File = null;

  constructor(public activeModal: NgbActiveModal, private httpService: HttpService) { }

  ngOnInit() {
  }

  handleFileInput(files: FileList) {
    this.fileToUpload = files.item(0);
  }

  uploadFile(){
    this.httpService.upload(this.username, this.id, this.fileToUpload).subscribe(
      message => {
        console.log(message.id);
      },
      error => {
        console.log(error.status);
      }
    );
  }

  closeModal() {
    this.activeModal.close('Modal Closed');
  }

}
