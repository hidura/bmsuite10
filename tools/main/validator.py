# -*- coding: utf8-*-

'''
Created on Ago 18, 2013

@author: hidura

'''

from .general import general


class validation:
    
    def patient(self, inputs, objName):
        error_msj = ""
        if objName == "addPatient":
            if "_name" not in inputs:
                error_msj += "El nombre del paciente no puede estar vacio"
            if "last_name" not in inputs:
                if error_msj != "":
                    error_msj += ", el Apellido del paciente no puede estar vacio"
                else:
                    error_msj = "El Apellido del paciente no puede estar vacio"
            
            if "birthdate" not in inputs:
                if error_msj != "":
                    error_msj += ", la fecha de nacimiento del paciente no puede estar vacio"
                else:
                    error_msj += "La fecha de nacimiento del paciente no puede estar vacio"
            
            if inputs["sex"] == "None":
            
                if error_msj != "":
                    error_msj += ", debe elegir el sexo de el paciente"
                else:
                    error_msj += "Debe elegir el sexo de el paciente"
            
            if "treatment" not in inputs:
                
                if error_msj != "":
                    error_msj += ", debe elegir un tipo de tratamiento para el paciente."
                else:
                    error_msj += "Debe elegir un tipo de tratamiento para el paciente."

            
            if "email" in inputs:
                if general().valEmail(inputs["email"]) == False:
                    if error_msj != "":
                        error_msj += ", correo electronico no valido."
                    else:
                        error_msj += "Correo electronico no valido."
           
            
            if inputs["race"] == "None":
                if error_msj != "":
                    
                    error_msj += ", debe elegir la raza de el paciente"
                else:
                    error_msj += "Debe elegir la raza de el paciente"
                    
            if inputs["civil_status"] == "None":
                if error_msj != "":
                    error_msj += ", debe elegir un estado civil para el paciente"
                else:
                    error_msj += "Debe elegir un estado civil para el paciente"
        elif objName == "addPicture":
            if "fileName" not in inputs:
                error_msj = "Debe tener una foto para subir."
                
            if "caseID" not in inputs:
                error_msj = "Debe tener un caso registrado antes de subir una foto."
                
            
        elif objName == "setParents":
            if "idPatient" not in inputs:
                error_msj = "Debe crear un caso antes de agregar, los padres."
                
        elif objName == "addTreaters":
            if "caseID" not in inputs:
                error_msj = "Debe crear un caso antes de agregar, los medicos tratantes."
        
        elif objName == "completeCatastrophic":
            if "caseID" not in inputs:
                error_msj = "Debe crear un caso antes de finalizar."
        
        
        elif objName == "delPicture":
            if "caseID" not in inputs:
                error_msj = "Debe crear un caso antes de borrar."
                        
        return self.retornoValidacion(error_msj)
        
    def validateDoctorInput(self, inputs, objName):
        error_msj = ""
        
        if objName == "addDoctor":
             
            if ("_name" not in inputs):
                error_msj = "El nombre del doctor no puede estar vac&#237;o"
            elif ("last_name" not in inputs):
                error_msj = "El apellido del doctor no puede estar vacio"
            elif ("id_card" not in inputs):
                error_msj = "La cedula del doctor no puede estar vacia"
            elif ("exequatur" not in inputs):
                error_msj = "El exequatur del doctor no puede estar vacio"
            elif ("birthdate" not in inputs):
                error_msj = "La fecha de nacimiento del doctor no puede estar vacia"
        
        return self.retornoValidacion(error_msj)
    
    def validateUserInput(self, inputs, objName):
        error_msj = ""
        
        if objName == "loginUser":
             
            if ("username" not in inputs):
                error_msj = "El nombre de usuario no puede estar vacio"
            elif ("password" not in inputs):
                error_msj = "El password no puede estar vacio"
        
        return self.retornoValidacion(error_msj)
    
    def retornoValidacion(self, errorvar):
        if errorvar != "":
            return [True, errorvar]
        else:
            return [False, None]
