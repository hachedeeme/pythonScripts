import os, re, config_parser


# =============================
# Congifs
# ============================================================================================================

config = config_parser.getConfigTree('ibox_paths.cfg')


# =============================
# Helper Functions
# ============================================================================================================

first_to_lowercase = lambda s: s[:1].lower() + s[1:] if s else ''
first_to_uppercase = lambda s: s[:1].upper() + s[1:] if s else ''
get_number = lambda s: filter(str.isdigit, s)

def to_snake_case(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

def to_res(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1-\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1-\2', s1).lower()

def contains(sub_string, string):
	return sub_string in string


# =============================
# Parent Class
# ============================================================================================================

class ABMFile():
	def __init__(self, className, pluralName, table):
		self.code = ""
		self.class_name  = className
		self.plural_name = pluralName
		self.table = table

	def addLine(self, aLine):
		self.code += ("\n" + aLine)

	def generateCode(self):
		raise NotImplementedError("Please Implement this method")

	def execute(self):
		self.generateCode()
		os.system('touch ' + self.path)
		abm_file = open(self.path, 'w')
		abm_file.write(self.code)
		abm_file.close()


# =============================
# Backend Controller
# ============================================================================================================

class ControllerFile(ABMFile):
	def __init__(self, className, pluralName):
		ABMFile.__init__(self, className, pluralName, {})
		self.path = config['backend']['controller'] + pluralName + 'Controller.php'
		print self.path

	def generateCode(self):
		code = """<?php

class MayPLURALNAMEController extends Trinomio_Rest_Controller {
	/**
 	 * @var Application_Model_MayCLASSNAME
 	 */
	protected $_model;

  public function init() {
		$this->_model = new Application_Model_MayCLASSNAME();
  }

  public function indexAction() {
  	$form = new Application_Form_MayCLASSNAMEList();
  	if ($form->isValid($this->_getAllParams())) {
			$this->view->SnakePLURALNAME = $this->_model->fetchByFilters($form->getValues())->toArray();
			$this->view->total_items = $this->_model->fetchCountByFilters($form->getValues());
		} else {
			$this->getResponse()->setHttpResponseCode(503);
			$this->view->error = $form->getMessages();
		}
	}

	public function getAction() {
		$id = $this->_getParam('id', '');
		$MinCLASSNAME = $this->_model->fetchById($id);
		if ($MinCLASSNAME) {
			$this->view->SnakeCLASSNAME = $MinCLASSNAME->toArray();
		} else {
			$this->getResponse()->setHttpResponseCode(404);
		}
	}

  public function postAction() {
		$form = new Application_Form_MayCLASSNAMEEdit();
		if ($form->isValid($this->_getAllParams())) {
			$this->view->SnakeCLASSNAME = $this->_model->insert($form->getValues())->toArray();
		} else {
			$this->view->error = $form->getMessages();
			$this->getResponse()->setHttpResponseCode(503);
		}
	}

	public function putAction() {
		$form = new Application_Form_MayCLASSNAMEEdit();
		if ($form->isValid($this->_getAllParams())) {
	  	$this->view->SnakeCLASSNAME = $this->_model->update($form->getValues())->toArray();
		} else {
			$this->getResponse()->setHttpResponseCode(503);
			$this->view->error = $form->getMessages();
		}
	}

	public function deleteAction() {
		$id = $this->_getParam('id', 0);
		$this->view->affectedRows = $this->_model->delete($id);
	}
}"""
		code = code.replace("MayCLASSNAME", self.class_name)
		code = code.replace("MinCLASSNAME", first_to_lowercase(self.class_name))
		code = code.replace("SnakeCLASSNAME", to_snake_case(self.class_name))
		code = code.replace("MayPLURALNAME", self.plural_name)
		code = code.replace("MinPLURALNAME", first_to_lowercase(self.plural_name))
		code = code.replace("SnakePLURALNAME",to_snake_case(self.plural_name))
		self.code = code


# =============================
# Backend Model
# ============================================================================================================

class ModelFile(ABMFile):
	def __init__(self, className, pluralName):
		ABMFile.__init__(self, className, pluralName, None)
		self.path = config['backend']['models'] + className + '.php'
		print self.path

	def generateCode(self):
		code = """<?php
		
class Application_Model_MayCLASSNAME {
	/**
 	 * @var Application_Model_DbTable_MayCLASSNAME
 	 */
	private $_dbTable;

	public function __construct() {
		$this->_dbTable = new Application_Model_DbTable_MayCLASSNAME();
	}

	public function fetchByFilters(array $form) {
		if ($form['pageSize'] === '-1') {
			return $this->_dbTable->fetchAll();
		}
		return $this->_dbTable->fetchAll(null, "{$form['sort']} {$form['sortOrder']}", 
			$form['pageSize'], $form['pageSize'] * ($form['page'] - 1));
	}

  public function fetchCountByFilters(array $form) {
    return $this->_dbTable->fetchCount(null);
  }

	public function fetchById($id) {
		return $this->_dbTable->fetchRow(array('id = ?' => $id));
	}

	public function insert(array $data) {
		$MinCLASSNAMEId = $this->_dbTable->insert($data);
		return $this->fetchById($MinCLASSNAMEId);
 }

	public function update(array $data) {
		$this->_dbTable->update($data, array('id = ?' => $data['id']));
		return $this->fetchById($data['id']);
	}

	public function delete($id) {
		return $this->_dbTable->delete(array('id = ?' => $id));
	}
}"""
		code = code.replace("MayCLASSNAME", self.class_name)
		code = code.replace("MinCLASSNAME", first_to_lowercase(self.class_name))
		self.code = code


# =============================
# Backend List Form
# ============================================================================================================

class FormListFile(ABMFile):
	def __init__(self, className, pluralName):
		ABMFile.__init__(self, className, pluralName, None)
		self.path = config['backend']['forms'] + className + 'List.php'
		print self.path

	def generateCode(self):
		code = """<?php
		
class Application_Form_MayCLASSNAMEList extends Zend_Form {

	/**
 	 * @var Zend_Form_Element_Xhtml
 	 */
	public $like;
	/**
	 * @var Zend_Form_Element_Xhtml
	 */
	public $page;
	/**
	 * @var Zend_Form_Element_Xhtml
	 */
	public $pageSize;
	/**
	 * @var Zend_Form_Element_Xhtml
	 */
	public $sort;
	/**
	 * @var Zend_Form_Element_Xhtml
	 */
	public $sortOrder;

	public function init() {
		$this->setName('MayCLASSNAMEList')->setMethod('get');
		$this->like = new Zend_Form_Element_Text('like');
		$this->like->setLabel('like');
		$this->addElement($this->like);

    $this->page = new Zend_Form_Element_Text('page');
    $this->page->setLabel('page');
    $this->addElement($this->page);

    $this->pageSize = new Zend_Form_Element_Text('pageSize');
    $this->pageSize->setLabel('pageSize');
    $this->addElement($this->pageSize);

    $this->sort = new Zend_Form_Element_Text('sort');
    $this->sort->setLabel('sort');
    $this->addElement($this->sort);

    $this->sortOrder = new Zend_Form_Element_Text('sortOrder');
    $this->sortOrder->setLabel('sortOrder');
    $this->addElement($this->sortOrder);
	}
}"""
		code = code.replace("MayCLASSNAME", self.class_name)
		self.code = code


# =============================
# Backend Edit Form
# ============================================================================================================

class FormEditFile(ABMFile):
	def __init__(self, className, pluralName, table):
		ABMFile.__init__(self, className, pluralName, table)
		self.path = config['backend']['forms'] + className + 'Edit.php'
		print self.path

	def generateCode(self):
		self.addLine("<?php")
		self.addLine("")
		self.addLine("class Application_Form_" + self.class_name + "Edit extends Zend_Form {")
		self.addLine("")
		self.declareVariables()
		self.addLine("")
		self.addLine("	public function init() {")
		self.addLine("		$this->setName('" + self.class_name + "Edit')->setMethod('post');")
		self.defineVariables()
		self.addLine("	}")
		self.addLine("}")

	def declareVariables(self):
		for key in self.table.keys():
			self.addLine("	/**")
			self.addLine("	 * @var Zend_Form_Element_Xhtml")
			self.addLine("	*/")
			self.addLine("	public $" + key + ";")

	def defineVariables(self):
		for key in self.table.keys():
			self.addLine("		$this->" + key + " = new Zend_Form_Element_Text('" + key + "');")
			self.addLine("		$this->" + key + "->setLabel('" + first_to_uppercase(key) + "');")
			fiel_type = self.table[key]
			if contains('varchar', fiel_type):
				len_field = get_number(fiel_type)
				self.addLine("		$this->" + key + "->addValidator('stringLength', false, array(0, " + len_field + "));")

			if key != 'id':
				self.addLine("		$this->" + key + "->setRequired(true);")
	
			self.addLine("		$this->addElement($this->" + key + ");")
			self.addLine("")


# =============================
# Backend Dbtable
# ============================================================================================================

class DBTableFile(ABMFile):
	def __init__(self, className, pluralName, table):
		ABMFile.__init__(self, className, pluralName, table)
		self.path = config['backend']['dbtables'] + className + '.php'
		print self.path

	def generateCode(self):
		self.code += "<?php\n\n/**"
		self.generateTable()
		code = """
*/
class Application_Model_DbTable_MayCLASSNAME extends Trinomio_DbTable_Abstract {

	protected $_name = 'SnakePLURALNAME';

}"""
		code = code.replace("MayCLASSNAME", self.class_name)
		code = code.replace("SnakePLURALNAME",to_snake_case(self.plural_name))
		self.code += code

	def generateTable(self):
		self.addLine("create table " + to_snake_case(self.plural_name) + " (")
		for key in self.table.keys():
			self.addLine("	" + key + " " + self.table[key] + ",")
		self.addLine("	primary key (id)")
		self.addLine(");")


# =============================
# Frontend Service
# ============================================================================================================

class ServiceFile(ABMFile):
	def __init__(self, className, pluralName):
		ABMFile.__init__(self, className, pluralName, None)
		self.path = config['frontend']['ng-services'] + first_to_lowercase(pluralName) + '.js'
		print self.path

	def generateCode(self):
		MinCLASSNAME  = first_to_lowercase(self.class_name)
		MinPLURALNAME = first_to_lowercase(self.plural_name)
		self.addLine("var speakersFrontApp = angular.module('speakersFrontApp');")
		self.addLine("")
		self.addLine("(function() {")
		self.addLine("")
		self.addLine("	'use strict';")
		self.addLine("")
		self.addLine("	/**")
		self.addLine("	 * @ngdoc function")
		self.addLine("	 * @name speakersFrontApp.factory:" + MinPLURALNAME + "Service")
		self.addLine("	 * @description")
		self.addLine("	 * # " + MinPLURALNAME + "Service")
		self.addLine("	 * Factory of the speakersFrontApp")
		self.addLine("	 */")
		self.addLine("	speakersFrontApp.factory('" + MinPLURALNAME + "Service', function(dbConnectedService, api2URL) {")
		self.addLine("		var instance = {")
		self.addLine("			serviceName: '" + to_res(self.plural_name) + "',")
		self.addLine("			uriToPut: function(" + MinCLASSNAME + ") {")
		self.addLine("				return this.serviceName + '/' + " + MinCLASSNAME + ".id;")
		self.addLine("			},")
		self.addLine("			url: api2URL")
		self.addLine("		};")
		self.addLine("		return angular.extend(angular.copy(dbConnectedService), instance);")
		self.addLine("	});")
		self.addLine("})();")


# =============================
# Frontend Edit Controller
# ============================================================================================================

class EditControllerFile(ABMFile):
	def __init__(self, className, pluralName):
		ABMFile.__init__(self, className, pluralName, None)
		self.path = config['frontend']['ng-controllers'] + first_to_lowercase(pluralName) + 'Edit.js'
		print self.path

	def generateCode(self):
		code = """var speakersFrontApp = angular.module('speakersFrontApp');

(function() {

	'use strict';

	/**
	 * @ngdoc function
	 * @name speakersFrontApp.controller:MayPLURALNAMEEditCtrl
	 * @description
	 * # MayPLURALNAMEEditCtrl
	 * Controller of the speakersFrontApp
	*/
	speakersFrontApp.controller('MayPLURALNAMEEditCtrl', function ($scope, MinPLURALNAMEService, data) {
		/* Controller definitions */
		$scope.data = {
			MinCLASSNAME : data.SnakeCLASSNAME,
			isNew: !('id' in data.SnakeCLASSNAME)
		};

		$scope.backToList = function(){
			window.location = '#/UrlPLURALNAME';
		};

		$scope.saveMayCLASSNAME = function(form){
			if (form.$valid) {
				MinPLURALNAMEService.save($scope.data.MinCLASSNAME, $scope.data.isNew).then(function(){
					window.location = '#/UrlPLURALNAME';
				});
			}
		};
	});
	
	speakersFrontApp.resolveMayPLURALNAMEEditCtrl = {
		data: function($route, MinPLURALNAMEService) {
			if ($route.current.params.id && $route.current.params.id.length > 0) {
				return MinPLURALNAMEService.fetchOne($route.current.params.id);
			} else {
				return { SnakeCLASSNAME: { } };
			}
		}
	};
})();"""
		code = code.replace('MayCLASSNAME' , self.class_name)
		code = code.replace('MinCLASSNAME' , first_to_lowercase(self.class_name))
		code = code.replace('MayPLURALNAME' , self.plural_name)
		code = code.replace('MinPLURALNAME' , first_to_lowercase(self.plural_name))
		code = code.replace('SnakeCLASSNAME' , to_snake_case(self.class_name))
		code = code.replace('MinTotalPLURALNAME' , self.plural_name.lower())
		code = code.replace('UrlPLURALNAME' , to_res(self.plural_name))
		self.code = code


# =============================
# Frontend List Controller
# ============================================================================================================

class ListControllerFile(ABMFile):
	def __init__(self, className, pluralName):
		ABMFile.__init__(self, className, pluralName, None)
		self.path = config['frontend']['ng-controllers'] + first_to_lowercase(pluralName) + 'List.js'
		print self.path

	def generateCode(self):
		code = """var speakersFrontApp = angular.module('speakersFrontApp');

(function() {

	'use strict';

	/**
	 * @ngdoc function
	 * @name speakersFrontApp.controller:MayPLURALNAMEListCtrl
	 * @description
	 * # MayPLURALNAMEListCtrl
	 * Controller of the speakersFrontApp
	 */
	speakersFrontApp.controller('MayPLURALNAMEListCtrl', function ($scope, $controller, MinPLURALNAMEService, MinPLURALNAMETable) {
		angular.extend(this, $controller('AbstractDbConnectedCtrl', { 
			$scope : $scope,
			currentService : MinPLURALNAMEService,
			currentTable : MinPLURALNAMETable,
			currentUrl : 'UrlPLURALNAME',
			deleteResolve: {
        title: function() {
          return 'Delete MayCLASSNAME';
        },
        message: function() {
          return 'Are you sure you want delete this MayCLASSNAME?'
        }
      }
		}));
	});
	
	speakersFrontApp.resolveMayPLURALNAMEListCtrl = {
		MinPLURALNAMETable: function($q, ngTableParams, MinPLURALNAMEService, tableService) {
			return tableService.createNgTableResolve($q, ngTableParams, function(count, page, sorting) {
				return MinPLURALNAMEService.fetchAll(count, page, sorting);
			}, {
				page: 1,
				count: 10,
				sorting: {
					id: 'asc'
				}
			}, function(data) {
				return data.SnakePLURALNAME;
			}
			);
		}
	};
})();"""
		code = code.replace('MayCLASSNAME', self.class_name)
		code = code.replace('MayPLURALNAME', self.plural_name)
		code = code.replace('MinPLURALNAME', first_to_lowercase(self.plural_name))
		code = code.replace('UrlPLURALNAME', to_res(self.plural_name))
		code = code.replace('SnakePLURALNAME', to_snake_case(self.plural_name))
		self.code = code


# =============================
# Frontend List View
# ============================================================================================================

class ListHtmlFile(ABMFile):
	def __init__(self, className, pluralName, table):
		ABMFile.__init__(self, className, pluralName, table)
		self.path = config['frontend']['ng-views'] + to_res(pluralName) + '-list.html'
		print self.path

	def generateCode(self):
		self.addLine('<div class="row">')
		self.addLine('  <div class="col-xs-9">')
		self.addLine('    <h1 style="margin-top:10px">' + self.class_name.upper() + '</h1>')
		self.addLine('	</div>')
		self.addLine('	<div class="col-xs-3">')
		self.addLine('		<div class="well">')
		self.addLine('			<button type="button" class="btn btn-default" ng-click="newItem()">')
		self.addLine('				<span class="glyphicon glyphicon-plus"></span> New ' + self.class_name)
		self.addLine('			</button>')
		self.addLine('		</div>')
		self.addLine('	</div>')
		self.addLine('</div> ')
		self.addLine('')
		self.generateTable()

	def generateTable(self):
		MinCLASSNAME  = first_to_lowercase(self.class_name)
		UrlPLURALNAME = to_res(self.plural_name)
		self.addLine('<table ng-table="table" class="table table-hover">')
		self.addLine('	<tr ng-repeat="' + MinCLASSNAME + ' in $data">')
		for key in self.table.keys():
			self.addLine('		<td data-title="' + "'" + first_to_uppercase(key) + "'" + '" sortable="'+ "'" + key + "'" + '">')
			self.addLine('			<div ng-bind="' + MinCLASSNAME + '.' + key + '"/>')
			self.addLine('		</td>')
		self.addLine('		<td style="width: 25%;">')
		self.addLine('			<a class="btn" href="#/' + UrlPLURALNAME + '/edit/{{' + MinCLASSNAME + '.id}}"><span class="glyphicon glyphicon-pencil"/></a>')
		self.addLine('			<a class="btn"ng-click="deleteItem(' + MinCLASSNAME + '.id)">   <span class="glyphicon glyphicon-trash"/></a>')
		self.addLine('		</td>')
		self.addLine('	</tr>')
		self.addLine('</table>')


# =============================
# Frontend Edit View
# ============================================================================================================

class EditHtmlFile(ABMFile):
	def __init__(self, className, pluralName, table):
		ABMFile.__init__(self, className, pluralName, table)
		self.path = config['frontend']['ng-views'] + to_res(pluralName) + '-edit.html'
		print self.path

	def generateCode(self):
		code = """<div class="row ng-scope">
  <div class="col-xs-9">
    <h1 style="margin-top:10px">MayCLASSNAME</h1>
  </div>
		<div class="col-xs-3">
      <div class="well">
        <div class="btn-group" uib-dropdown>
          <button id="split-button" type="button" class="btn btn-default"
          	ng-init="relatedRecordSelected = relatedRecordSelected || relatedRecords[0]"
            ng-bind="relatedRecordSelected.buttonTitle" ng-click="relatedRecordSelected.add()"></button>
          <button type="button" class="btn btn-default" uib-dropdown-toggle>
            <span class="caret"></span>
            <span class="sr-only">Split button!</span>
          </button>
          <ul uib-dropdown-menu role="menu" aria-labelledby="split-button">
            <li role="menuitem" ng-repeat="relatedRecord in relatedRecords">
              <a href="" ng-click="relatedRecord.add()" ng-bind="relatedRecord.buttonTitle"></a>
            </li>
          </ul>
        </div>
      </div>
  </div>
</div>
"""
		
		self.code = code.replace('MayCLASSNAME', self.class_name.upper())

		self.addLine('<form name="form" class="form form-horizontal" novalidate ng-submit="save' + self.class_name + '(form)">')
		self.addLine('<div class="row">')
		self.addLine('	<div class="col-md-4">')
		self.addLine('		<h4>General</h4>')
		self.generateFields()
		self.addLine('	</div>')
		self.addLine('')
		self.addLine('	<div class="col-md-8">')
		self.addLine('    <!-- PARAMETRIC FIELDS -->')
		self.addLine('	</div>')
		self.addLine('')
		self.addLine('</div>')
		self.addLine('<div class="row">')
		self.addLine('	<div class="col-md-6">')
		self.addLine('		<div class="form-group">')
		self.addLine('			<div class="col-md-offset-3 col-md-9">')
		self.addLine('				<button type="submit" class="btn btn-primary"> Save ' + self.class_name + ' </button>')
		self.addLine('				<button type="button" class="btn btn-default" ng-click="backToList()"> Back to List </button>')
		self.addLine('			</div>')
		self.addLine('		</div>')
		self.addLine('	</div>')
		self.addLine('</div>')
		self.addLine('</form>')

	def generateFields(self):
		MinCLASSNAME  = first_to_lowercase(self.class_name)
		for key in self.table.keys():
			if key != 'id':
				fiel_type  = self.table[key]
				input_text = '				<input type="text" name="' + key + '" class="form-control" ng-model="data.' + MinCLASSNAME + '.' + key + '" placeholder="' + first_to_uppercase(key) + '"'
				
				if contains('varchar', fiel_type):
					input_text += ' required maxlength="' + get_number(fiel_type) + '" />'
				else:
					input_text += ' required/>'

				self.addLine('		<div class="form-group">')
				self.addLine('			<label class="label-control col-md-3" for="' + key + '"> ' + first_to_uppercase(key) + ' </label>')
				self.addLine('			<div class="col-md-9">')
				self.addLine(input_text)
				self.addLine('				<span class="error-message" ng-show="form.$submitted && form.' + key + '.$error.required">This field is required</span>')
				self.addLine('			</div>')
				self.addLine('		</div>')


# =============================
# Factories
# ============================================================================================================

class ABMCreator(object):
	def __init__(self, className, pluralName, table):
		self.class_name  = className
		self.plural_name = pluralName
		self.files = []
		self.table = table

	# ======================================================
	# === Backend files
	# ======================================================
	def modelFile(self):
		self.files.append(ModelFile(self.class_name, self.plural_name))
		return self

	def dbTableFile(self):
		self.files.append(DBTableFile(self.class_name, self.plural_name, self.table))
		return self

	def formListFile(self):
		self.files.append(FormListFile(self.class_name, self.plural_name))
		return self

	def formEditFile(self):
		self.files.append(FormEditFile(self.class_name, self.plural_name, self.table))
		return self

	def controllerFile(self):
		self.files.append(ControllerFile(self.class_name, self.plural_name))
		return self

	def backendABM(self):
		return self.modelFile().dbTableFile().formListFile().formEditFile().controllerFile()

	# ======================================================
	# === Frontend files
	# ======================================================

	def serviceFile(self):
		self.files.append(ServiceFile(self.class_name, self.plural_name))
		return self

	def editControllerFile(self):
		self.files.append(EditControllerFile(self.class_name, self.plural_name))
		return self

	def listControllerFile(self):
		self.files.append(ListControllerFile(self.class_name, self.plural_name))
		return self

	def listHtmlFile(self):
		self.files.append(ListHtmlFile(self.class_name, self.plural_name, self.table))
		return self

	def editHtmlFile(self):
		self.files.append(EditHtmlFile(self.class_name, self.plural_name, self.table))
		return self

	def frontendABMFile(self):
		return self.serviceFile().editControllerFile().listControllerFile().listHtmlFile().editHtmlFile()

	# ======================================================
	# === Full ABMS
	# ======================================================
	def fullABM(self):
		return self.backendABM().frontendABMFile().appJsIndexInfo()

	def appJsIndexInfo(self):
		MayPLURALNAME = self.plural_name
		MinPLURALNAME = first_to_lowercase(self.plural_name)
		ResPLURALNAME = to_res(self.plural_name)
		UrlPLURALNAME = to_res(self.plural_name)

		print("")
		print(".when('/" + UrlPLURALNAME + "',{")
		print("	 templateUrl: 'views/" + ResPLURALNAME + "-list.html',")
		print("	 controller : '" + MayPLURALNAME + "ListCtrl',")
		print("  resolve: speakersFrontApp.resolve" + MayPLURALNAME + "ListCtrl,")
		print("}).when('/" + UrlPLURALNAME + "/edit/:id',{")
		print("  templateUrl: 'views/" + ResPLURALNAME + "-edit.html',")
		print("  controller : '" + MayPLURALNAME + "EditCtrl',")
		print("  resolve: speakersFrontApp.resolve" + MayPLURALNAME + "EditCtrl")
		print("}).when('/" + UrlPLURALNAME + "/new',{")
		print("	 templateUrl: 'views/" + ResPLURALNAME + "-edit.html',")
		print("  controller : '" + MayPLURALNAME + "EditCtrl',")
		print("	 resolve: speakersFrontApp.resolve" + MayPLURALNAME + "EditCtrl")
		print("})")
		print("")
		print('<li ng-class="getNavSidebarClassItem(' + "'/" + UrlPLURALNAME + "')" + '"' + '><a ng-href="#/' + UrlPLURALNAME + '">' + self.plural_name + '</a></li>')
		print("")
		print('<script src="scripts/services/' + MinPLURALNAME + '.js"></script>')
		print("")
		print('<script src="scripts/controllers/' + MinPLURALNAME + 'List.js"></script>')
		print("")
		print('<script src="scripts/controllers/' + MinPLURALNAME + 'Edit.js"></script>')
		print('')
		return self

	def onTheFlyChanges(self, entityName, entityPluralName):
		code = """------------------------------------------------------------------
in: app/views/UrlPLURALNAME-edit.html
<a href="" ng-click="newEntityMayCLASSNAME()">New EntityMayCLASSNAME</a>

------------------------------------------------------------------
in: app/scripts/controllers/MinPLURALNAMEEdit.js
$scope.newEntityMayCLASSNAME = function() {
	var modalInstance = $uibModal.open({
		templateUrl: 'views/EntityMinPLURALNAME-edit.html',
		controller: 'EntityMayPLURALNAMEEditCtrl',
		size: 'lg',
		resolve: angular.extend(angular.copy(speakersFrontApp.absResolveEntityMayPLURALNAMEEditCtrl), {
			data: function($route, EntityMinPLURALNAMEService) {
				return { EntityMinCLASSNAME: {} }; //Needs the empty case of app/scripts/controllers/EntityMayCLASSNAMEEdit.js
			}
		})
	});

	modalInstance.result.then(function(response) {
		console.log(response);
		$scope.EntityMinPLURALNAME.push(response.EntityMinCLASSNAME);
		$scope.data.MinCLASSNAME.EntityMinCLASSNAMEId = response.EntityMinCLASSNAME.id;
	});
}

------------------------------------------------------------------
in: app/scripts/controllers/EntityMayCLASSNAMEEdit.js

add $uibModalInstance to the parameters of controller.

$scope.backToList = function(){
	if ($uibModalInstance) {
		$uibModalInstance.dismiss();
	} else {
		window.location = '#/EntityMinPLURALNAME';
	}
};

$scope.saveEntityMayCLASSNAME = function(form){
	if (form.$valid) {
		EntityMinPLURALNAMEService.save($scope.data.EntityMinCLASSNAME, $scope.data.isNew).then(function(response){
			if ($uibModalInstance) {
				$uibModalInstance.close(response);
			} else {
				window.location = '#/EntityMinPLURALNAME';
			}
		});
	}
};

speakersFrontApp.resolveEntityMayPLURALNAMEEditCtrl = angular.extend(angular.copy(speakersFrontApp.absResolveEntityMayPLURALNAMEEditCtrl), {
  $uibModalInstance: function(){
    return null;
  },
});
"""
		code = code.replace('EntityMayCLASSNAME', entityName)
		code = code.replace('EntityMinCLASSNAME', first_to_lowercase(entityName))
		code = code.replace('EntityMayPLURALNAME', entityPluralName)
		code = code.replace('EntityMinPLURALNAME', first_to_lowercase(entityPluralName))
		code = code.replace('MayCLASSNAME', self.class_name)
		code = code.replace('MinCLASSNAME', first_to_lowercase(self.class_name))
		code = code.replace('MayPLURALNAME', self.plural_name)
		code = code.replace('MinPLURALNAME', first_to_lowercase(self.plural_name))
		code = code.replace('UrlPLURALNAME', to_res(self.plural_name))
		code = code.replace('SnakePLURALNAME', to_snake_case(self.plural_name))
		print(code)
		
	def execute(self):
		for abm_file in self.files:
			abm_file.execute()
			print("generated " + abm_file.path)


# =============================
# MAIN
# ============================================================================================================

if __name__ == "__main__":
	
	# USER
	userProperties = {}
	userProperties['id']    = 'integer not null auto_increment'
	userProperties['email'] = 'varchar(100)'
	userProperties['pass']  = 'varchar(100)'
	userProperties['passSalt']    = 'varchar(100)'
	userProperties['firstname']   = 'varchar(100)'
	userProperties['lastname']    = 'varchar(100)'
	userProperties['countryCode'] = 'varchar(3)'
	userProperties['company']  = 'varchar(100)'
	userProperties['area']     = 'varchar(100)'
	userProperties['position'] = 'varchar(100)'
	userProperties['image']    = 'varchar(255)'
	userProperties['creationDate'] = 'timestamp'
	userProperties['status'] = "enum('active', 'inactive', 'deleted')"
	# ABMCreator('User', 'Users', userProperties).fullABM().execute()

	speakerProperties = {}
	speakerProperties['id'] = 'integer not null auto_increment'
	speakerProperties['bureauId']   = 'integer'
	speakerProperties['timezoneId'] = 'integer'
	speakerProperties['firstName']= 'varchar(50)'
	speakerProperties['lastName'] = 'varchar(50)'
	speakerProperties['company']  = 'varchar(50)'
	speakerProperties['skype']    = 'varchar(50)'
	speakerProperties['sex']      = "enum('','Male','Female')"
	speakerProperties['birthday'] = 'date'
	speakerProperties['birthdayAlert'] = "bit(1)"
	speakerProperties['nationality']   = 'varchar(3)'
	speakerProperties['countryCode']   = 'varchar(3)'
	speakerProperties['address']  = 'varchar(256)'
	speakerProperties['shortBio'] = 'varchar(256)'
	speakerProperties['bio'] = 'text'
	speakerProperties['website'] = 'varchar(128)'
	speakerProperties['active']  = "bit(1)"
	# ABMCreator('Speaker', 'Speakers', speakerProperties).fullABM().execute()

	speakerContactsProperties = {}
	speakerContactsProperties['id'] = 'integer not null auto_increment'
	speakerContactsProperties['speakerId'] = 'integer'
	speakerContactsProperties['contactId'] = 'integer'
	# ABMCreator('SpeakerContact', 'SpeakerContacts', speakerContactsProperties).dbTableFile().execute()

	speakerEmailProperties = {}
	speakerEmailProperties['id'] = 'integer not null auto_increment'
	speakerEmailProperties['speakerId'] = 'integer'
	speakerEmailProperties['type']      = "enum('Work','Personal')"
	speakerEmailProperties['email']     = "varchar(50)"
	# ABMCreator('SpeakerEmail', 'SpeakerEmails', speakerEmailProperties).dbTableFile().execute()

	speakerPhonesProperties = {}
	speakerPhonesProperties['id'] = 'integer not null auto_increment'
	speakerPhonesProperties['speakerId']   = 'integer'
	speakerPhonesProperties['type']        = "enum('Home','Work','Mobile','Fax')"
	speakerPhonesProperties['phonenumber'] = "varchar(50)"
	# ABMCreator('SpeakerPhone', 'SpeakerPhones', speakerPhonesProperties).dbTableFile().execute()

	themeProperties = {}
	themeProperties['id'] = 'integer not null auto_increment'
	themeProperties['name'] = 'varchar(20)'
	# ABMCreator('Theme', 'Themes', themeProperties).fullABM().execute()

	bureauProperties = {}
	bureauProperties['id'] = 'integer not null auto_increment'
	bureauProperties['name'] = 'varchar(256)'
	bureauProperties['abbreviation'] = 'varchar(3)'
	bureauProperties['active']       = 'bit(1)'
	# ABMCreator('Bureau', 'Bureaux', bureauProperties).fullABM().execute()

	speakerThemeProperties = {}
	speakerThemeProperties['id'] = 'integer not null auto_increment'
	speakerThemeProperties['speakerId'] = 'integer'
	speakerThemeProperties['themeId']   = 'integer'
	# ABMCreator('SpeakerTheme', 'SpeakerThemes', speakerThemeProperties).dbTableFile().execute()

	requirementTypeProperties = {}
	requirementTypeProperties['id'] = 'integer not null auto_increment'
	requirementTypeProperties['name'] = 'varchar(30)'
	# ABMCreator('RequirementType', 'RequirementTypes', requirementTypeProperties).fullABM().execute()

	speakerRequirementProperties = {}
	speakerRequirementProperties['id'] = 'integer not null auto_increment'
	speakerRequirementProperties['speakerId']   = 'integer'
	speakerRequirementProperties['typeId']      = 'integer'
	speakerRequirementProperties['description'] = 'varchar(200)'
	# ABMCreator('SpeakerRequirement', 'SpeakerRequirements', speakerRequirementProperties).dbTableFile().execute()

	# ABMCreator('Event','Events',{}).onTheFlyChanges('Venue','Venues')
	# ABMCreator('Event','Events',{}).onTheFlyChanges('Contact','Contacts')
	# ABMCreator('Subevent','Subevents',{}).onTheFlyChanges('Contact','Contacts')
	# ABMCreator('Subevent','Subevents',{}).onTheFlyChanges('Speaker','Speakers')
	# ABMCreator('Subevent','Subevents',{}).onTheFlyChanges('Sponsor','Sponsors')
	# ABMCreator('Sponsor','Sponsors',{}).onTheFlyChanges('Contact','Contacts')
	# ABMCreator('Contact','Contacts',{}).onTheFlyChanges('Bureau','Bureaux')
	# ABMCreator('Speaker','Speakers',{}).onTheFlyChanges('Contact','Contacts')
	# ABMCreator('Speaker','Speakers',{}).onTheFlyChanges('Theme','Themes')
	# ABMCreator('Speaker','Speakers',{}).onTheFlyChanges('Requirement','Requirements')
	# ABMCreator('Venue','Venues',{}).onTheFlyChanges('Contact','Contacts')

	timezoneProperties = {}
	timezoneProperties['id'] = 'integer not null auto_increment'
	timezoneProperties['name']     = 'varchar(44)'
	timezoneProperties['timezone'] = 'varchar(30)'
	# ABMCreator('Timezone', 'Timezones', timezoneProperties).fullABM().execute()

	companionProperties = {}
	companionProperties['fromDate'] = 'timestamp'
	companionProperties['toDate']   = 'timestamp'
	companionProperties['price']    = 'numeric(10,2)'
	companionProperties['type']     = "enum('transfer', 'hotel', 'flight')"
	companionProperties['detail']   = 'varchar(30)'
	# ABMCreator('CompanionLogistic', 'CompanionLogistics', companionProperties).serviceFile().listHtmlFile().listControllerFile().execute()

	countryProperties = {}
	countryProperties['code'] = 'varchar(3)'
	countryProperties['name'] = 'varchar(100)'
	countryProperties['iso_3166_1_alpha_2_code'] = 'varchar(2)'
	# ABMCreator('Country', 'Countries', countryProperties).fullABM().execute()

	idTypesProperties = {}
	idTypesProperties['id']   = 'integer not null auto_increment'
	idTypesProperties['name'] = 'varchar(20)'
	# ABMCreator('IdType', 'IdTypes', idTypesProperties).fullABM().execute()

	# ABMCreator('EventHome', 'EventsHome', {}).listControllerFile().listHtmlFile().execute()
