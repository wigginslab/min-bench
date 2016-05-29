gapi.analytics.ready(function() {

  gapi.analytics.createComponent('PropertySelector', {

    /**
     * Initialize the PropertySelector instance and render it to the page.
     * @return {PropertySelector} The instance.
     */
    execute: function() {
      let options = this.get();

      // Allow container to be a string ID or an HTMLElement.
      this.container = typeof options.container == 'string' ?
        document.getElementById(options.container) : options.container;

      // Allow the template to be overridden.
      if (options.template) this.template = options.template;

      this.container.innerHTML = this.template;
      this.propertyInput = this.container.querySelector('select');

      this.getProperties();

      this.container.onchange = this.onChange.bind(this);
      return this;
    },

    onChange: function() {
      if (this.propertyInput.selectedIndex == -1) {
        return;
      }
      
      let selected_index = this.propertyInput.selectedIndex;
      let property_id = this.propertyInput.options[selected_index].value;
      this.emit('change', 'ga:' + property_id);
    },

    /*
     * Requests a list of all properties for the authorized user.
     */
    getProperties: function() {
      var request = gapi.client.analytics.management.profiles.list({
        'accountId': '~all',
        'webPropertyId': '~all'
      });
      request.execute(this.propertyCallback.bind(this));
    },

    /*
     * The results of the list method are passed as the results object.
     * The following code shows how to iterate through them.
     */
    propertyCallback: function(results) {
      if (results && !results.error) {
        var properties = results.items;
        console.log('All properties for user');
        console.log(properties);
        for (var i = 0, property; property = properties[i]; i++) {
          var opt = document.createElement('option');
          opt.innerHTML = property.websiteUrl ? property.websiteUrl : property.name;
          opt.value = property.id;
          this.propertyInput.appendChild(opt);
        }
      }
      this.onChange();    // Call this to render the chart for default id
    },

    /**
     * The html structure used to build the component. Developers can
     * override this by passing it to the component constructor.
     */
    template:
      '<select></select>'
  });

});

