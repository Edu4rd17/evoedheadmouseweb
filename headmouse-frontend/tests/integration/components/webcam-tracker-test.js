import { module, test } from 'qunit';
import { setupRenderingTest } from 'headmouse-frontend/tests/helpers';
import { render } from '@ember/test-helpers';
import { hbs } from 'ember-cli-htmlbars';

module('Integration | Component | webcam-tracker', function (hooks) {
  setupRenderingTest(hooks);

  test('it renders', async function (assert) {
    // Set any properties with this.set('myProperty', 'value');
    // Handle any actions with this.set('myAction', function(val) { ... });

    await render(hbs`<WebcamTracker />`);

    assert.dom().hasText('');

    // Template block usage:
    await render(hbs`
      <WebcamTracker>
        template block text
      </WebcamTracker>
    `);

    assert.dom().hasText('template block text');
  });
});
