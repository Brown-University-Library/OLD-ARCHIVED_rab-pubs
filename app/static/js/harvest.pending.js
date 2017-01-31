harvest.pending = (function() {

    var
      configMap = {
        pending_model : null
      },

      stateMap = {},

      jqueryMap = {},

      loadPending, makePendingList,

      onClickPendingDetailsModal,
      initializeModel,
      setJqueryMap, initModule;


    setJqueryMap = function() {
      var 
        $sources = $('.api-source');
        jqueryMap = {
          'sources' : {},
          $modal : $('#modalDetails'),
          $table : $('#detailsTableBody'),
        };

      $.each($sources, function( i, source ) {
        var rabid = $( this ).data('rabid');
        var $panel = $( this ).find('.pending-collapse');

        jqueryMap.sources[rabid] = $panel;
      });
    };

    makePendingList = function( jsonList ) {
      var list_items = [];

      jsonList.forEach( function( pendingObj ) {
        var pendingObj,
            $li, $title, $venue, $date,
            $modal_btn, $col1, $col2;

        $li = $('<li/>', {  'class'       : 'list-group-item pending-list-item',
                            'data-source' : pendingObj.source,
                            'data-exid'   : pendingObj.exid,
                          });
        $title = $('<h5/>', { 'class' : 'pending-title',
                                'text'  : pendingObj.display.short.title });
        $venue = $('<span/>', { 'class' : 'pending-venue',
                                'text'  : pendingObj.display.short.venue });
        $date = $('<span/>', {  'class' : 'pending-date',
                                'text'  : pendingObj.display.short.date });
        $modal_btn = $('<button/>', { 'type'        : 'button',
                                      'class'       : 'btn btn-primary details-modal-btn',
                                      'data-exid'   : pendingObj.exid,
                                      'html'        : '<span class="glyphicon glyphicon-plus"></span>'
                                    });

        $col1 = $('<span/>', { 'class' : 'pending-list-col' });
        $col2 = $('<span/>', { 'class' : 'pending-list-col' });
        
        $modal_btn.on('click', function(e) {
          e.preventDefault();

          var exid = $( this ).data('exid');
          onClickPendingDetailsModal( exid );
        });

        $col1.append($title);
        $col1.append($venue);
        $col1.append($date);
        $col2.append($modal_btn);

        $li.append($col1);
        $li.append($col2);

        list_items.push( $li );
      });

      return list_items;
    };

    loadPending = function (source) {
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

    initializeModel = function () {
      for (var rabid in jqueryMap.sources) {
        $panel = jqueryMap.sources[rabid];
        var count = $panel.data('pending-count');
        if (count > 0) {
          configMap.pending_model.initialize( rabid );
        }
      }
    };

    onClickPendingDetailsModal = function ( exid ) {
      var
        $modal, $table,
        pendingObj;
      
      $modal = jqueryMap.$modal;
      $table = jqueryMap.$table;
      $table.empty();

      pendingObj = configMap.pending_model.get( {'exid' : exid.toString() });
      pendingObj.display.details.forEach( function( detailsObj ) {
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

    configModule = function ( map ) {
      configMap.pending_model = map.pending_model;
    };

    initModule = function () {
      setJqueryMap();

      initializeModel();
    };

    return {
      loadPending: loadPending,
      configModule: configModule,
      initModule: initModule
    };
}());