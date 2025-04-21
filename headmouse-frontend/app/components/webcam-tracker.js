import Component from '@ember/component'; // Use classic component for lifecycle hook
import { action } from '@ember/object';

export default class WebcamTrackerComponent extends Component {
    @action
    didInsertElement() {
        super.didInsertElement(...arguments);
        let img = document.getElementById('face-mesh-feed');
        if (img) {
            img.src = 'http://localhost:5000/video_feed';
        }
    }
    // @action
    // didInsertElement() {
    //     const video = document.getElementById('webcam');

    //     if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
    //         navigator.mediaDevices.getUserMedia({ video: true })
    //             .then((stream) => {
    //                 video.srcObject = stream;
    //             })
    //             .catch((err) => {
    //                 console.error('Error accessing webcam:', err);
    //             });
    //     }
    // }
}
