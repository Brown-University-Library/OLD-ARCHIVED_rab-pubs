harvest.queries = (function() {

    var
      configMap = {
        queries_model : null
      },

      stateMap = {},

      jqueryMap = {},

      loadQueries, makeQueriesList,

      onClickNewQueryField,
      makeNewQueryField,

      onClickQueryDetailsModal,
      onClickNewQueryModal,
      initializeModel,
      setJqueryMap, initModule;


    setJqueryMap = function() {
      var 
        $sources = $('.api-source');
        jqueryMap = {
          'sources' : {},
          $modal : $('#modalQueries'),
          $form : $('#modalQueriesForm'),
          $add_field : $('#addFieldButton')
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
                            'data-source' : queryObj.source,
                            'data-exid'   : pendingObj.exid,
                          });
        $title = $('<h5/>', { 'class' : 'queries-title',
                                'text'  : queryObj.display.short.title });
        $modal_btn = $('<button/>', { 'type'        : 'button',
                                      'class'       : 'btn btn-primary query-modal-btn',
                                      'data-rabid'   : queryObj.rabid,
                                      'html'        : 'Search details'
                                    });

        $modal_btn.on('click', function(e) {
          e.preventDefault();

          var exid = $( this ).data('rabid');
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

    // onClickQueriesDetailsModal = function ( rabid ) {
    //   var
    //     $modal, $form,
    //     queryObj;
      
    //   $modal = jqueryMap.$modal;
    //   $form = jqueryMap.$form;
    //   $form.empty();

    //   queryObj = configMap.pending_model.get( {'rabid' : rabid.toString() });
    //   queryObj.display.details.forEach( function( detailsObj ) {
    //       $tr = $('<tr/>');
    //       $key = $('<th/>', { 'scope': 'row',
    //                           'text' : detailsObj.key });
    //       $value = $('<td/>', { 'text' : detailsObj.value });

    //       $tr.append($key);
    //       $tr.append($value);
    //       $form.append($tr);
    //   });
    //   $modal.modal('show');
    // };

    makeNewQueryField = function ( params ) {
      var
        $form_group, $input_group,
        $select, $input;

      $form_group = $('<div/>', {'class': 'form-group'});
      $input_group = $('<div/>', {'class': 'input-group search-param'});
      $select = $('<select/>', { 'class': 'form-control param' });
      $text_input = $('<input/>', { 'class' : 'form-control param-value',
                                    'type'  : 'text'});

      $input_group.append($select).append($text_input);
      $form_group.append($input_group);

      params.forEach( function( param ) {
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
        $add_field, queryObj;
      
      $modal = jqueryMap.$modal;
      $form = jqueryMap.$form;

      $form.empty();
      $form.data('source', src);

      queryObj = configMap.queries_model.get( {'source' : src.toString(), 'new': true });
      $form_group = makeNewQueryField( queryObj.params );
      $form.append($form_group);
      
      $modal.modal('show');
    };

    onClickNewQueryField = function ( $form ) {
      var src = $form.data('source');
      queryObj = configMap.queries_model.get( {'source' : src.toString(), 'new': true });
      $form_group = makeNewQueryField( queryObj.params );
      $form.append($form_group);

      return true;
    };

    initializeModel = function () {
      for (var rabid in jqueryMap.sources) {
          configMap.queries_model.initialize( rabid );
      }
    };

    configModule = function ( map ) {
      configMap.queries_model = map.queries_model;
    };

    initModule = function () {
      setJqueryMap();

      initializeModel();

      $('#addFieldButton').on('click', function(e){
        e.preventDefault();

        onClickNewQueryField( jqueryMap.$form );
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