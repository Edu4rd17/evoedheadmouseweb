import Route from '@ember/routing/route';

export default class ApplicationRoute extends Route {
    async model() {
        const response = await fetch('https://evoedheadmouseweb-2111207bc088.herokuapp.com/');
        const data = await response.json();
        return data;
    }
}
