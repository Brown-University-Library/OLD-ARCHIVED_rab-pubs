harvest.queries = (function() {

    var
      configMap = {
        queries_model : null
      },

      stateMap = {},

      jqueryMap = {},

      loadQueries, makeQueriesList,

      onClickQueryDetailsModal,
      onClickNewQueryModal, on
      setJqueryMap, initModule;


    setJqueryMap = function() {
      var 
        $sources = $('.api-source');
        jqueryMap = {
          'sources' : {},
          $modal : $('#modalQueries'),
          $table : $('#modalQueriesTableBody'),
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

        sourceData = configMap.pending_model.all( {'source' : source} );
        $lis = makePendingList( sourceData );
        $list = $('<ol/>', {'class' : 'list-group'});
        $lis.forEach( function($li) {
          $list.append($li);
        });

        $target = jqueryMap.sources[ source ];
        $target.append($list);     
    };

    onClickQueriesDetailsModal = function ( rabid ) {
      var
        $modal, $table,
        queryObj;
      
      $modal = jqueryMap.$modal;
      $table = jqueryMap.$table;
      $table.empty();

      queryObj = configMap.pending_model.get( {'rabid' : rabid.toString() });
      queryObj.display.details.forEach( function( detailsObj ) {
          $tr = $('<tr/>');
          $key = $('<th/>', { 'scope': 'row',
                              'text' : detailsObj.key });
          $value = $('<td/>', { 'text' : detailsObj.value });

          $tr.append($key);
          $tr.append($value);
          $table.append($tr);
      });
      $modal.modal('show');
    };

    onClickNewQueryModal = function ( src ) {
      var
        $modal, $table,
        queryObj;
      
      $modal = jqueryMap.$modal;
      $table = jqueryMap.$table;
      $table.empty();

      queryObj = configMap.query_model.get( {'source' : source.toString(), 'new': true });
      queryObj.parameters.forEach( function( paramObj ) {
          $tr = $('<tr/>');
          $key = $('<th/>', { 'scope': 'row',
                              'text' : paramObj.key });
          $value = $('<td/>', { 'text' : '' });

          $tr.append($key);
          $tr.append($value);
          $table.append($tr);
      });
      $modal.modal('show');
    };

    configModule = function ( map ) {
      configMap.query_model = map.query_model;
    };

    initModule = function () {
      setJqueryMap();

      configMap.query_model.initialize();

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