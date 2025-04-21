import Route from '@ember/routing/route';

export default class ApplicationRoute extends Route {
    async model() {
        const response = await fetch('http://localhost:5000/');
        const data = await response.json();
        return data;
    }
}
