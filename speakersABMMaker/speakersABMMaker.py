import os
import re

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

# ============================================================================================================
class ControllerFile(ABMFile):
	def __init__(self, className, pluralName):
		ABMFile.__init__(self, className, pluralName, {})
		self.path = 'backend/application/controllers/' + pluralName + 'Controller.php'

	def generateCode(self):
		MayCLASSNAME  = self.class_name
		MinCLASSNAME  = first_to_lowercase(self.class_name)
		MinPLURALNAME = first_to_lowercase(self.plural_name)
		self.addLine("<?php")
		self.addLine("")
		self.addLine("class " + self.plural_name + "Controller extends Trinomio_Rest_Controller {")
		self.addLine("	/**")
		self.addLine(" 	 * @var Application_Model_" + MayCLASSNAME)
		self.addLine(" 	 */")
		self.addLine("	protected $_model;")
		self.addLine("")
		self.addLine("  public function init() {")
		self.addLine("		$this->_model = new Application_Model_" + MayCLASSNAME + "();")
		self.addLine("  }")
		self.addLine("")
		self.addLine("  public function indexAction() {")
		self.addLine("  	$form = new Application_Form_" + MayCLASSNAME + "List();")
		self.addLine("  	if ($form->isValid($this->_getAllParams())) {")
		self.addLine("			$this->view->" + to_snake_case(MinPLURALNAME) + " = $this->_model->fetchByFilters($form->getValues())->toArray();")
		self.addLine("		} else {")
		self.addLine("			$this->getResponse()->setHttpResponseCode(503);")
		self.addLine("			$this->view->error = $form->getMessages();")
		self.addLine("		}")
		self.addLine("	}")
		self.addLine("")
		self.addLine("	public function getAction() {")
		self.addLine("		$id = $this->_getParam('id', '');")
		self.addLine("		$" + MinCLASSNAME + " = $this->_model->fetchById($id);")
		self.addLine("		if ($" + MinCLASSNAME + ") {")
		self.addLine("			$this->view->" + to_snake_case(MinCLASSNAME) + " = $" + MinCLASSNAME + "->toArray();")
		self.addLine("		} else {")
		self.addLine("			$this->getResponse()->setHttpResponseCode(404);")
		self.addLine("		}")
		self.addLine("	}")
		self.addLine("")
		self.addLine("  public function postAction() {")
		self.addLine("		$form = new Application_Form_" + MayCLASSNAME + "Edit();")
		self.addLine("		if ($form->isValid($this->_getAllParams())) {")
		self.addLine("			$this->view->" + to_snake_case(MinCLASSNAME) + " = $this->_model->insert($form->getValues())->toArray();")
		self.addLine("		} else {")
		self.addLine("			$this->view->error = $form->getMessages();")
		self.addLine("			$this->getResponse()->setHttpResponseCode(503);")
		self.addLine("		}")
		self.addLine("	}")
		self.addLine("")
		self.addLine("	public function putAction() {")
		self.addLine("		$form = new Application_Form_" + MayCLASSNAME + "Edit();")
		self.addLine("		if ($form->isValid($this->_getAllParams())) {")
		self.addLine("	  	$this->view->" + to_snake_case(MinCLASSNAME) + " = $this->_model->update($form->getValues())->toArray();")
		self.addLine("		} else {")
		self.addLine("			$this->getResponse()->setHttpResponseCode(503);")
		self.addLine("			$this->view->error = $form->getMessages();")
		self.addLine("		}")
		self.addLine("	}")
		self.addLine("")
		self.addLine("	public function deleteAction() {")
		self.addLine("		$id = $this->_getParam('id', 0);")
		self.addLine("		$this->view->affectedRows = $this->_model->delete($id);")
		self.addLine("	}")
		self.addLine("}")

# ============================================================================================================
class ModelFile(ABMFile):
	def __init__(self, className, pluralName):
		ABMFile.__init__(self, className, pluralName, None)
		self.path = 'backend/application/models/' + className + '.php'

	def generateCode(self):
		MayCLASSNAME  = self.class_name
		MinCLASSNAME  = first_to_lowercase(self.class_name)
		self.addLine("<?php")
		self.addLine("")
		self.addLine("class Application_Model_" + MayCLASSNAME + " {")
		self.addLine("	/**")
		self.addLine(" 	 * @var Application_Model_DbTable_" + MayCLASSNAME)
		self.addLine(" 	 */")
		self.addLine("	private $_dbTable;")
		self.addLine("")
		self.addLine("	public function __construct() {")
		self.addLine("		$this->_dbTable = new Application_Model_DbTable_" + MayCLASSNAME + "();")
		self.addLine("	}")
		self.addLine("")
		self.addLine("	public function fetchByFilters(array $form) {")
		self.addLine("		return $this->_dbTable->fetchAll();")
		self.addLine("	}")
		self.addLine("")
		self.addLine("	public function fetchById($id) {")
		self.addLine("		return $this->_dbTable->fetchRow(array('id = ?' => $id));")
		self.addLine("	}")
		self.addLine("")
		self.addLine("	public function insert(array $data) {")
		self.addLine("		$" + MinCLASSNAME + "Id = $this->_dbTable->insert($data);")
		self.addLine("		return $this->fetchById($" + MinCLASSNAME + "Id);")
		self.addLine(" }")
		self.addLine("")
		self.addLine("	public function update(array $data) {")
		self.addLine("		$this->_dbTable->update($data, array('id = ?' => $data['id']));")
		self.addLine("		return $this->fetchById($data['id']);")
		self.addLine("	}")
		self.addLine("")
		self.addLine("	public function delete($id) {")
		self.addLine("		return $this->_dbTable->delete(array('id = ?' => $id));")
		self.addLine("	}")
		self.addLine("}")

# ============================================================================================================
class FormListFile(ABMFile):
	def __init__(self, className, pluralName):
		ABMFile.__init__(self, className, pluralName, None)
		self.path = 'backend/application/forms/' + className + 'List.php'

	def generateCode(self):
		table_name = first_to_lowercase(self.plural_name)
		self.addLine("<?php")
		self.addLine("")
		self.addLine("class Application_Form_" + self.class_name + "List extends Zend_Form {")
		self.addLine("")
		self.addLine("	/**")
		self.addLine(" 	 * @var Zend_Form_Element_Xhtml")
		self.addLine(" 	 */")
		self.addLine("	public $like;")
		self.addLine("")
		self.addLine("	public function init() {")
		self.addLine("		$this->setName('" + self.class_name + "List')->setMethod('get');")
		self.addLine("		$this->like = new Zend_Form_Element_Text('like');")
		self.addLine("		$this->like->setLabel('like');")
		self.addLine("		$this->addElement($this->like);")
		self.addLine("	}")
		self.addLine("}")

# ============================================================================================================
class FormEditFile(ABMFile):
	def __init__(self, className, pluralName, table):
		ABMFile.__init__(self, className, pluralName, table)
		self.path = 'backend/application/forms/' + className + 'Edit.php'

	def generateCode(self):
		table_name = first_to_lowercase(self.plural_name)
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

# ============================================================================================================
class DBTableFile(ABMFile):
	def __init__(self, className, pluralName, table):
		ABMFile.__init__(self, className, pluralName, table)
		self.path = 'backend/application/models/DbTable/' + className + '.php'

	def generateCode(self):
		self.addLine("<?php")
		self.addLine("")
		self.addLine("/**")
		self.generateTable()
		self.addLine("*/")
		self.addLine("class Application_Model_DbTable_" + self.class_name + " extends Zend_Db_Table_Abstract {")
		self.addLine("")
		self.addLine("	protected $_name = '"+ to_snake_case(self.plural_name) + "';")
		self.addLine("")
		self.addLine("}")

	def generateTable(self):
		self.addLine("create table " + to_snake_case(self.plural_name) + " (")
		for key in self.table.keys():
			self.addLine("	" + key + " " + self.table[key] + ",")
		self.addLine("	primary key (id)")
		self.addLine(");")

# ============================================================================================================
class ServiceFile(ABMFile):
	def __init__(self, className, pluralName):
		ABMFile.__init__(self, className, pluralName, None)
		self.path = 'frontend/app/scripts/services/' + first_to_lowercase(pluralName) + '.js'

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

# ============================================================================================================
class EditControllerFile(ABMFile):
	def __init__(self, className, pluralName):
		ABMFile.__init__(self, className, pluralName, None)
		self.path = 'frontend/app/scripts/controllers/' + first_to_lowercase(pluralName) + 'Edit.js'

	def generateCode(self):
		MinCLASSNAME  = first_to_lowercase(self.class_name)
		MayPLURALNAME = self.plural_name
		MinPLURALNAME = first_to_lowercase(self.plural_name)
		self.addLine("var speakersFrontApp = angular.module('speakersFrontApp');")
		self.addLine("")
		self.addLine("(function() {")
		self.addLine("	'use strict';")
		self.addLine("")
		self.addLine("	/**")
		self.addLine("	 * @ngdoc function")
		self.addLine("	 * @name speakersFrontApp.controller:" + MayPLURALNAME + "EditCtrl")
		self.addLine("	 * @description")
		self.addLine("	 * # " + MayPLURALNAME + "EditCtrl")
		self.addLine("	 * Controller of the speakersFrontApp")
		self.addLine("		*/")
		self.addLine("	speakersFrontApp.controller('" + MayPLURALNAME + "EditCtrl', function ($scope, " + MinPLURALNAME + "Service, data) {")
		self.addLine("		/* Controller definitions */")
		self.addLine("		$scope.data = {")
		self.addLine("			" + MinCLASSNAME + " : data." + to_snake_case(self.class_name) + ",")
		self.addLine("			isNew: !('id' in data." + to_snake_case(self.class_name) + ")")
		self.addLine("		};")
		self.addLine("")
		self.addLine("		$scope.backToList = function(){")
		self.addLine("			window.location = '#/" + MinPLURALNAME.lower() + "';")
		self.addLine("		};")
		self.addLine("")
		self.addLine("		$scope.save" + self.class_name + " = function(){")
		self.addLine("			" + MinPLURALNAME + "Service.save($scope.data." + MinCLASSNAME + ", $scope.data.isNew).then(function(){")
		self.addLine("				window.location = '#/" + MinPLURALNAME.lower() + "';")
		self.addLine("			});")
		self.addLine("		};")
		self.addLine("	});")
		self.addLine("	")
		self.addLine("	speakersFrontApp.resolve" + MayPLURALNAME + "EditCtrl = {")
		self.addLine("		data: function($route, " + MinPLURALNAME + "Service) {")
		self.addLine("			if ($route.current.params.id && $route.current.params.id.length > 0) {")
		self.addLine("				return " + MinPLURALNAME + "Service.fetchOne($route.current.params.id);")
		self.addLine("			} else {")
		self.addLine("				return { " + to_snake_case(self.class_name) + ": { } };")
		self.addLine("			}")
		self.addLine("		}")
		self.addLine("	};")
		self.addLine("})();")

# ============================================================================================================
class ListControllerFile(ABMFile):
	def __init__(self, className, pluralName):
		ABMFile.__init__(self, className, pluralName, None)
		self.path = 'frontend/app/scripts/controllers/' + first_to_lowercase(pluralName) + 'List.js'

	def generateCode(self):
		MinCLASSNAME  = first_to_lowercase(self.class_name)
		MayPLURALNAME = self.plural_name
		MinPLURALNAME = first_to_lowercase(self.plural_name)
		self.addLine("var speakersFrontApp = angular.module('speakersFrontApp');")
		self.addLine("(function() {")
		self.addLine("")
		self.addLine("	'use strict';")
		self.addLine("")
		self.addLine("	/**")
		self.addLine("	 * @ngdoc function")
		self.addLine("	 * @name speakersFrontApp.controller:" + MayPLURALNAME + "ListCtrl")
		self.addLine("	 * @description")
		self.addLine("	 * # " + MayPLURALNAME + "ListCtrl")
		self.addLine("	 * Controller of the speakersFrontApp")
		self.addLine("	 */")
		self.addLine("	speakersFrontApp.controller('" + MayPLURALNAME + "ListCtrl', function ($scope, $controller, " + MinPLURALNAME + "Service, " + MinPLURALNAME + "Table) {")
		self.addLine("		angular.extend(this, $controller('AbstractDbConnectedCtrl', { ")
		self.addLine("			$scope : $scope,")
		self.addLine("			currentService : " + MinPLURALNAME + "Service,")
		self.addLine("			currentTable : " + MinPLURALNAME + "Table,")
		self.addLine("			currentUrl : '" + MinPLURALNAME.lower() + "'")
		self.addLine("		}));")
		self.addLine("	});")
		self.addLine("	")
		self.addLine("	speakersFrontApp.resolve" + MayPLURALNAME + "ListCtrl = {")
		self.addLine("		" + MinPLURALNAME + "Table: function($q, ngTableParams, " + MinPLURALNAME + "Service, tableService) {")
		self.addLine("			return tableService.createNgTableResolve($q, ngTableParams, function(count, page, sorting) {")
		self.addLine("				return " + MinPLURALNAME + "Service.fetchAll(count, page, sorting);")
		self.addLine("			}, {")
		self.addLine("				page: 1,")
		self.addLine("				count: 10,")
		self.addLine("				sorting: {")
		self.addLine("					country_code: 'asc'")
		self.addLine("				}")
		self.addLine("			}, function(data) {")
		self.addLine("				return data." + to_snake_case(self.plural_name) + ";")
		self.addLine("			}")
		self.addLine("			);")
		self.addLine("		}")
		self.addLine("	};")
		self.addLine("})();")

# ============================================================================================================
class ListHtmlFile(ABMFile):
	def __init__(self, className, pluralName, table):
		ABMFile.__init__(self, className, pluralName, table)
		self.path = 'frontend/app/views/' + to_res(pluralName) + '-list.html'

	def generateCode(self):
		MinCLASSNAME  = first_to_lowercase(self.class_name)
		MayPLURALNAME = self.plural_name
		MinPLURALNAME = first_to_lowercase(self.plural_name)
		self.addLine('<div class="well">')
		self.addLine('	<div class="row">')
		self.addLine('		<div class="col-xs-6">')
		self.addLine('			<button type="button" class="btn btn-default" ng-click="newItem()">')
		self.addLine('				<span class="glyphicon glyphicon-plus"></span> New ' + self.class_name)
		self.addLine('			</button>')
		self.addLine('		</div>')
		self.addLine('		<div class="col-xs-6"></div>')
		self.addLine('	</div>')
		self.addLine('</div> ')
		self.addLine('')
		self.generateTable()

	def generateTable(self):
		MinCLASSNAME  = first_to_lowercase(self.class_name)
		MinPLURALNAME = first_to_lowercase(self.plural_name)
		self.addLine('<table ng-table="table" class="table table-hover">')
		self.addLine('	<tr ng-repeat="' + MinCLASSNAME + ' in $data">')
		for key in self.table.keys():
			self.addLine('		<td data-title="' + "'" + first_to_uppercase(key) + "'" + '" sortable="'+ "'" + key + "'" + '">')
			self.addLine('			<div ng-bind="' + MinCLASSNAME + '.' + key + '"/>')
			self.addLine('		</td>')
		self.addLine('		<td style="width: 25%;">')
		self.addLine('			<a class="btn" href="#/' + MinPLURALNAME.lower() + '/edit/{{' + MinCLASSNAME + '.id}}"><span class="glyphicon glyphicon-pencil"/></a>')
		self.addLine('			<a class="btn"ng-click="deleteItem(' + MinCLASSNAME + '.id)">   <span class="glyphicon glyphicon-trash"/></a>')
		self.addLine('		</td>')
		self.addLine('	</tr>')
		self.addLine('</table>')

# ============================================================================================================
class EditHtmlFile(ABMFile):
	def __init__(self, className, pluralName, table):
		ABMFile.__init__(self, className, pluralName, table)
		self.path = 'frontend/app/views/' + to_res(pluralName) + '-edit.html'

	def generateCode(self):
		self.addLine('<form name="form" class="main-form">')
		self.generateFields()
		self.addLine('	<button class="btn btn-primary" ng-click="save' + self.class_name + '()"> Save ' + self.class_name + ' </button>')
		self.addLine('	<button class="btn btn-default" ng-click="backToList()"> Back to List </button>')
		self.addLine('</form>')

	def generateFields(self):
		MinCLASSNAME  = first_to_lowercase(self.class_name)
		MinPLURALNAME = first_to_lowercase(self.plural_name)
		for key in self.table.keys():
			if key != 'id':
				self.addLine('	<div class="form-group">')
				self.addLine('		<label> ' + self.class_name + ' ' + first_to_uppercase(key) + ' </label>')
				self.addLine('		<input type="text" class="form-control" ng-model="data.' + MinCLASSNAME + '.' + key + '" placeholder="' + self.class_name + ' ' + first_to_uppercase(key) + '"/>')
				self.addLine('	</div>')

# ============================================================================================================
class ABMCreator(object):
	def __init__(self, className, pluralName, table):
		self.class_name  = className
		self.plural_name = pluralName
		self.files = []
		self.table = table
		self.initialize()

	def initialize(self):
		# Backend
		#self.files.append(ModelFile(self.class_name, self.plural_name))
		#self.files.append(DBTableFile(self.class_name, self.plural_name, self.table))
		#self.files.append(FormListFile(self.class_name, self.plural_name))
		self.files.append(FormEditFile(self.class_name, self.plural_name, self.table))
		self.files.append(ControllerFile(self.class_name, self.plural_name))
		# Frontend
		# self.files.append(ServiceFile(self.class_name, self.plural_name))
		# self.files.append(EditControllerFile(self.class_name, self.plural_name))
		# self.files.append(ListControllerFile(self.class_name, self.plural_name))
		# self.files.append(ListHtmlFile(self.class_name, self.plural_name, self.table))
		# self.files.append(EditHtmlFile(self.class_name, self.plural_name, self.table))

	def execute(self):
		for abm_file in self.files:
			abm_file.execute()
			print("generated " + abm_file.path)

		MayPLURALNAME = self.plural_name
		MinPLURALNAME = first_to_lowercase(self.plural_name)
		ResPLURALNAME = to_res(self.plural_name)
		print("")
		print(".when('/" + MinPLURALNAME.lower() + "',{")
		print("	 templateUrl: 'views/" + ResPLURALNAME + "-list.html',")
		print("	 controller : '" + MayPLURALNAME + "ListCtrl',")
		print("  resolve: speakersFrontApp.resolve" + MayPLURALNAME + "ListCtrl,")
		print("}).when('/" + MinPLURALNAME.lower() + "/edit/:id',{")
		print("  templateUrl: 'views/" + ResPLURALNAME + "-edit.html',")
		print("  controller : '" + MayPLURALNAME + "EditCtrl',")
		print("  resolve: speakersFrontApp.resolve" + MayPLURALNAME + "EditCtrl")
		print("}).when('/" + MinPLURALNAME.lower() + "/new',{")
		print("	 templateUrl: 'views/" + ResPLURALNAME + "-edit.html',")
		print("  controller : '" + MayPLURALNAME + "EditCtrl',")
		print("	 resolve: speakersFrontApp.resolve" + MayPLURALNAME + "EditCtrl")
		print("})")
		print("")
		print('<li ng-class="getNavSidebarClassItem(' + "'/" + MinPLURALNAME.lower() + "')" + '"' + '><a ng-href="#/' + MinPLURALNAME.lower() + '">' + self.plural_name + '</a></li>')
		print("")
		print('<script src="scripts/services/' + MinPLURALNAME + '.js"></script>')
		print("")
		print('<script src="scripts/controllers/' + MinPLURALNAME + 'List.js"></script>')
		print("")
		print('<script src="scripts/controllers/' + MinPLURALNAME + 'Edit.js"></script>')

# ============================================================================================================

table = {}
table['id']     = 'integer not null auto_increment'
table['name']   = 'varchar(50)'
table['cityId'] = 'integer'
table['address']= 'varchar(200)'
table['phone']  = 'varchar(50)'
table['fax']    = 'varchar(50)'
table['email']  = 'varchar(50)'
table['web']    = 'varchar(50)'
table['mobile'] = 'varchar(100)'


# create table car_agencies (
# 	id integer not null auto_increment,
# 	cityId integer,
# 	name varchar(50),
# 	address varchar(200),
# 	phone varchar(50),
# 	mobile varchar(100)
# 	fax varchar(50),
# 	email varchar(50),
# 	web varchar(50),
# 	primary key (id)
# );

creator = ABMCreator('CarAgencie', 'CarAgencies', table)
creator.execute()


# x = """    public function getAction() {
#         $code = $this->_getParam('id', '');
#         $MinCLASSNAME = $this->_model->fetchByCode($code);
#         if ($MinCLASSNAME) {
#             $this->view->MinCLASSNAME = $MinCLASSNAME->toArray();
#         } else {
#             $this->getResponse()->setHttpResponseCode(404);
#         }
#     }
# 
#     public function postAction() {
#         $form = new Application_Form_MayCLASSNAMEEdit();
#         if ($form->isValid($this->_getAllParams())) {
#             $this->view->MinCLASSNAME = $this->_model->insert($form->getValues())->toArray();
# 
#         } else {
#             $this->view->error = $form->getMessages();
#             $this->getResponse()->setHttpResponseCode(503);
#         }
#     }
# """
# x = x.replace("MayCLASSNAME", "Currency")
# x = x.replace("MinCLASSNAME", "currency")
# 
# print(x)