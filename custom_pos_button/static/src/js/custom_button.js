odoo.define('custom_pos_button.CustomButton', function (require) {
    'use strict';

    const PosComponent = require('point_of_sale.PosComponent');
    const ProductScreen = require('point_of_sale.ProductScreen');
    const { useListener } = require('@web/core/utils/hooks');
    const Registries = require('point_of_sale.Registries');

    // Define the custom button component
    class CustomButton extends PosComponent {
        setup() {
            super.setup();
            useListener('click', this.onClick);
        }

        async onClick() {
            // Action when the button is clicked
            this.showPopup('TextInputPopup', {
                title: 'Custom Button Clicked',
                body: 'Hello! You clicked the custom button!',
            });
        }
    }

    CustomButton.template = 'CustomButtonTemplate';

    // Register the component
    Registries.Component.add(CustomButton);

    // Extend ProductScreen to include the button
    Registries.Component.extend(ProductScreen, class extends ProductScreen {
        setup() {
            super.setup();
        }
    });

    // Define the OWL template for the button
    const { xml } = owl;
    Registries.Component.addTemplate('CustomButtonTemplate', xml`
        <div class="control-button">
            <button class="btn btn-primary">Custom Button</button>
        </div>
    `);

    return CustomButton;
});