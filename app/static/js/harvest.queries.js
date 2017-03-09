harvest.queries = (function() {

    var
      configMap = {
        queries_model : null,
        params_model : null
      },

      stateMap = {},

      jqueryMap = {},

      loadQueries, makeQueriesList,

      onClickNewQueryField,
      onClickRemoveQueryField,
      makeNewQueryField,

      onClickQueryDetailsModal,
      onClickNewQueryModal,
      onClickSubmitNewQuery,
      initializeModel,
      setJqueryMap, initModule;


    setJqueryMap = function() {
      var 
        $sources = $('.api-source');
        jqueryMap = {
          'sources' : {},
          $modal : $('#modalQueries'),
          $form : $('#modalQueriesForm'),
          $save_query : $('#saveQueryButton'),
        };

      $.each($sources, function( i, source ) {
        var rabid = $( this ).data('rabid');
        var $panel = $( this ).find('.queries-collapse');

        jqueryMap.sources[rabid] = $panel;
      });
    };

    makeQueriesList = function( jsonList ) {
      var list_items = [];

      jsonList.forEach( function( queryObj ) {
        var $li, $title, $modal_btn;

        $li = $('<li/>', {  'class'       : 'list-group-item queries-list-item',
                            'data-source' : queryObj.source
                          });
        $title = $('<h5/>', { 'class' : 'queries-title',
                                'text'  : queryObj.display });
        $modal_btn = $('<button/>', { 'type'        : 'button',
                                      'class'       : 'btn btn-primary query-modal-btn',
                                      'data-rabid'   : queryObj.rabid,
                                      'html'        : '\&plus\;'
                                    });

        $modal_btn.on('click', function(e) {
          e.preventDefault();

          var rabid = $( this ).data('rabid');
          onClickQueryDetailsModal( rabid );
        });

        $li.append($title);
        $li.append($modal_btn);

        list_items.push( $li );
      });

      return list_items;
    };

    loadQueries = function (source) {
      var sourceData,
        $lis, $list, $target;

        sourceData = configMap.queries_model.all( {'source' : source} );
        $lis = makeQueriesList( sourceData );
        $list = $('<ol/>', {'class' : 'list-group'});
        $lis.forEach( function($li) {
          $list.append($li);
        });

        $target = jqueryMap.sources[ source ];
        $target.append($list);     
    };

    onClickQueryDetailsModal = function ( rabid ) {
       var
         $modal, $table,
         queryObj, data;
      
       $modal = jqueryMap.$modal;
       $table = $('<table/>');
       $body = $modal.find('.modal-body');
       $body.empty()

       queryObj = configMap.queries_model.get( {'rabid' : rabid.toString() });
       data = queryObj.data;
       for (const attr of Object.keys(data)) {
           if (data[ attr ].length === 0 ) {
             continue;
           } else {
             $tr = $('<tr/>');
             $key = $('<th/>', { 'scope': 'row',
                                 'text' : attr });
             $value = $('<td/>', { 'text' : data[ attr ] });

             $tr.append($key);
             $tr.append($value);
             $table.append($tr);
	  }
       };

       $body.append($table);
       $modal.modal('show');
    };

    makeNewQueryField = function ( params ) {
      var
        $form_group, $input_group,
        $select, $input, $rmv_button;

      $form_group = $('<div/>', {'class': 'form-group'});
      $input_group = $('<div/>', {'class': 'input-group search-param'});
      $select = $('<select/>', { 'class': 'form-control param' });
      $text_input = $('<input/>', { 'class' : 'form-control param-value',
                                    'type'  : 'text'});
      $rmv_button = $('<button/>', {  'class' : 'btn btn-danger remove-param',
                                      'type'  : 'button',
                                      'html'  : '\&times\;' });

      $rmv_button.on('click', function(e) {
        e.preventDefault();
        $form_group.remove();
      });

      $input_group.append($select).append($text_input).append($rmv_button);
      $form_group.append($input_group);

      params.forEach( function(param) {
        var $option;
        $option = $('<option/>', {'value' : param,
                                  'text'  : param});
        $select.append($option);
      });

      return $form_group;
    };

    onClickNewQueryModal = function ( src ) {
      var
        $modal, $form, $form_group,
        $label_group, $label_name, $label_input,
        $add_field, queryObj;
      
      $modal = jqueryMap.$modal;
      $body = $modal.find('.modal-body');
      $body.empty()
      $form = $('<form/>');

      $form.data('source', src);

      $label_group = $('<div/>', {'class': 'form-group search-param'});
      $label_name = $('<label/>', { 'class' : 'param',
                                    'for'   : 'queryLabel',
                                    'text'  : 'name'});
      $label_input = $('<input/>', {'class' : 'form-control param-value',
                                    'type'  : 'text',
                                    'id'    : 'queryLabel',
                                    'value' : 'Default search'});
      $label_group.append($label_name).append($label_input);
      $form.append($label_group);

      queryObj = configMap.queries_model.get( {'source' : src.toString() });
      $form_group = makeNewQueryField( queryObj.params );
      $form.append($form_group);
      
      $body.append($form);

      $add_field_btn = $('<button/>', {	'type'	: 'button',
					'class'	: 'btn btn-primary',
					'text'	: '\&plus\;' });
      $add_field_btn.on('click', function(e) {
	e.preventDefault();
        onClickNewQueryField($form);
      });

      $body.append($add_field_btn);
      $modal.modal('show');
    };

    onClickNewQueryField = function ( $form ) {
      var src = $form.data('source');
      queryObj = configMap.queries_model.get( {'source' : src.toString() });
      $form_group = makeNewQueryField( queryObj.params );
      $form.append($form_group);

      return true;
    };

    onClickSaveQuery = function ( $form ) {
      var
        $inputs, src,
        form_data = {};

      form_data['label'] = $form.find('#queryLabel').val();

      $inputs = $form.find('.input-group');
      $inputs.each( function( idx ) {
        var param, param_val;
        param = $(this).find('select option:selected').val();
        param_val = $(this).find('input.param-value').val();

        form_data[param] = param_val;
      });

      src = $form.data('source');
      configMap.queries_model.create(src, form_data);
    };

    initializeModel = function () {
      for (var rabid in jqueryMap.sources) {
          configMap.queries_model.initialize( rabid );
      }
    };

    configModule = function ( map ) {
      configMap.queries_model = map.queries_model;
      configMap.params_model = map.params_model;
    };

    initModule = function () {
      setJqueryMap();

      initializeModel();

      $('#saveQueryButton').on('click', function(e){
        e.preventDefault();
        var $form = jqueryMap.$modal.find('form');
        onClickSaveQuery( $form );
      });

      $('.new-query-modal-btn').on('click', function(e){
        e.preventDefault();

        var src = $( this ).data('harvest-source');
        onClickNewQueryModal( src );
      });
    };

    return {
      loadQueries: loadQueries,
      configModule: configModule,
      initModule: initModule
    };
}());
