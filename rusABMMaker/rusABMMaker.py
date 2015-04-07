first_to_lowercase = lambda s: s[:1].lower() + s[1:] if s else ''

def stringVariable(aVariable):
	return '"' + aVariable + '"'

class AbmCode():
	def __init__(self, className, variables):
		self.code = ""
		self.class_name = className
		self.variables = variables

	def param_name(self):
		return first_to_lowercase(self.class_name)

	def addLine(self, aLine):
		self.code += ("\n" + aLine)

	def generateInstanceVariables(self):
		for varName in self.variables.keys():
			self.addLine("	private " + variables.get(varName) + " " + varName + ";")

	def addSeparator(self):
		self.addLine("")
		self.addLine("-------------------------------------------------------------------------")
		self.addLine("")

	def generateClassCode(self):
		self.addLine("import javax.persistence.Entity;")
		self.addLine("import javax.persistence.Table;")
		self.addLine("")
		self.addLine("import coop.tecso.foundation.persistence.model.AbstractPersistentObject;")
		self.addLine("")
		self.addLine("@Entity")
		self.addLine("@Table(name=" + stringVariable("sin_" + self.param_name()) + ")")
		self.addLine("public class " + self.class_name + " extends AbstractPersistentObject{")
		self.addLine("")
		self.generateInstanceVariables()
		self.addLine("}")

	def generateDAOCode(self):
		self.addLine("import java.util.List;")
		self.addLine("")
		self.addLine("import coop.tecso.search.service.impl.PagedFinder;")
		self.addLine("")
		self.addLine("public interface " + self.class_name + "DAO {")
		self.addLine("")
		self.addLine("	PagedFinder searchPaginado(PagedFinder pf);")
		self.addLine("")
		self.addLine("	List<" + self.class_name + "> findAll();")
		self.addLine("")
		self.addLine("	" + self.class_name + " findById(Long id);")
		self.addLine("")
		self.addLine("	void save(" + self.class_name + " " + self.param_name() + ");")
		self.addLine("")
		self.addLine("	void delete(" + self.class_name + " " + self.param_name() + ");")
		self.addLine("}")

	def generateDAOImplCode(self):
		self.addLine("import java.util.List;")
		self.addLine("")
		self.addLine("@Repository")
		self.addLine("public class " + self.class_name + "DAOImpl extends PersistentObjectDAOImpl<" + self.class_name + "> implements " + self.class_name + "DAO {")
		self.addLine("")
		self.addLine("	@Override")
		self.addLine("	public List<" + self.class_name + "> findAll() {")
		self.addLine("		return super.findAll(" + self.class_name + ".class);")
		self.addLine("	}")
		self.addLine("")
		self.addLine("	@Override")
		self.addLine("	public " + self.class_name + " findById(Long id) {")
		self.addLine("		return super.findById(" + self.class_name + ".class, id);")
		self.addLine("	}")
		self.addLine("")
		self.addLine("	public PagedFinder searchPaginado(PagedFinder pf) {")
		self.addLine("		DetachedCriteria criteria = this.setearFiltros(pf.getFilter());")
		self.addLine("		pf.setCount(super.countByCriteria(criteria).intValue());")
		self.addLine("		criteria = this.setearFiltros(pf.getFilter());")
		self.addLine("		CommonGeneralUtil.addOrderToFilter(criteria, pf.getFilter());")
		self.addLine("		pf.setResultList(super.findByCriteria(criteria, pf.getFirstResult(), pf.getMaxResult()));")
		self.addLine("		return pf;")
		self.addLine("	}")
		self.addLine("	")
		self.generateSetterFilters()
		self.addLine("}")


	def generateSetterFilters(self):
		self.addLine("	private DetachedCriteria setearFiltros(FinderFilter filter) {")
		self.addLine("		DetachedCriteria criteria = DetachedCriteria.forClass(" + self.class_name + ".class);")
		self.addLine("		")
		for varName in self.variables.keys():
			varType = variables.get(varName)
			self.addLine("		" + varType + " " + varName + " = (" + varType + ") " + "filter.getFilterValue(" + stringVariable(varName) + ");")
			if varType == 'String':
				self.addLine("		if(!StringUtil.isNullOrEmpty(" + varName + ")){")
			else:
				self.addLine("		if(" + varName + " != null){")
			self.addLine("			criteria.add(Restrictions.eq(" + stringVariable(varName) + ", " + varName + "));")
			self.addLine("		}")
			self.addLine("")
		self.addLine("		return criteria;")
		self.addLine("	}")

	def generateServiceCode(self):
		self.addLine("import java.util.List;")
		self.addLine("")
		self.addLine("import coop.tecso.search.service.impl.PagedFinder;")
		self.addLine("")
		self.addLine("public interface " + self.class_name + "Service {")
		self.addLine("")
		self.addLine("	PagedFinder searchPaginado(PagedFinder pf);")
		self.addLine("")
		self.addLine("	List<" + self.class_name + "> findAll();")
		self.addLine("")
		self.addLine("	" + self.class_name + " findById(Long id);")
		self.addLine("")
		self.addLine("	void save(" + self.class_name + " " + self.param_name() + ");")
		self.addLine("")
		self.addLine("	void delete(" + self.class_name + " " + self.param_name() + ");")
		self.addLine("}")

	def generateServiceImplCode(self):
		dao = self.param_name() + "DAO"
		self.addLine("import java.util.List;")
		self.addLine("")
		self.addLine("import javax.annotation.Resource;")
		self.addLine("")
		self.addLine("import org.springframework.stereotype.Service;")
		self.addLine("import org.springframework.transaction.annotation.Transactional;")
		self.addLine("")
		self.addLine("import coop.tecso.search.service.impl.PagedFinder;")
		self.addLine("")
		self.addLine("@Service(" + stringVariable(self.param_name() + "Service") + ")")
		self.addLine("@Transactional")
		self.addLine("public class " + self.class_name + "ServiceImpl implements " + self.class_name + "Service {")
		self.addLine("	@Resource")
		self.addLine("	private " + self.class_name + "DAO " + dao + ";")
		self.addLine("")
		self.addLine("	@Override")
		self.addLine("	public List<" + self.class_name + "> findAll() {")
		self.addLine("		return " + dao + ".findAll();")
		self.addLine("	}")
		self.addLine("")
		self.addLine("	@Override")
		self.addLine("	public " + self.class_name + " findById(Long id) {")
		self.addLine("		return " + dao + ".findById(id);")
		self.addLine("	}")
		self.addLine("")
		self.addLine("	@Override")
		self.addLine("	public void save(" + self.class_name + " " + self.param_name() + "){")
		self.addLine("		" + dao + ".save(" + self.param_name() + ");")
		self.addLine("	}")
		self.addLine("")
		self.addLine("	@Override")
		self.addLine("	public void delete(" + self.class_name + " " + self.param_name() + "){")
		self.addLine("		" + dao + ".delete(" + self.param_name() + ");")
		self.addLine("	}")
		self.addLine("	@Override")
		self.addLine("	public PagedFinder searchPaginado(PagedFinder pf) {")
		self.addLine("		return " + dao + ".searchPaginado(pf);")
		self.addLine("	}")
		self.addLine("}")


className = 'ParametroSiniestroHecho'
variables = {
		'parametroSiniestro':'ParametroSiniestro',
		'hechoGenerador':'HechoGenerador',
		'subHechoGenerador':'SubHechoGenerador'
		}

abm = AbmCode(className, variables)
abm.generateClassCode()
abm.addSeparator()
abm.generateDAOCode()
abm.addSeparator()
abm.generateDAOImplCode()
abm.addSeparator()
abm.generateServiceCode()
abm.addSeparator()
abm.generateServiceImplCode()

print(abm.code)