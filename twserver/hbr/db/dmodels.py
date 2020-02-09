# -*- coding: latin1 -*-
"""
Created on Tue Sep 29 05:23:52 2015

@author: ricardo
"""

def rem_acentuacao(str):
    try:
        from unicodedata import normalize
        return normalize('NFKD', str.decode('utf-8')).encode('ASCII', 'ignore')
    
    except:
        return str

class Hospede(models.Model):
    
    uuid          = models.CharField(max_length=50, default = make_uuid, primary_key=True)
    data_cadastro = models.DateTimeField(default = datetime.datetime.now())

    Nome         = models.CharField(max_length=100)
    Cpf          = models.CharField(max_length=100, null=False, unique=True, blank=True)
    Rg           = models.CharField(max_length=100, null=True, blank=True)
    Naturalidade = models.CharField(max_length=100, null=True, blank=True)
    Nascimento   = models.DateTimeField(null=True, blank=True)
    Nacionalidade= models.CharField(max_length=100, null=True, blank=True)
    
    Profissao    = models.CharField(max_length=100, null=True, blank=True)
    Empresa      = models.CharField(max_length=100, null=True, blank=True)
    
    CarroPlaca   = models.CharField(max_length=100, null=True, blank=True)
    Procedencia  = models.CharField(max_length=100, null=True, blank=True)
    Destino      = models.CharField(max_length=100, null=True, blank=True)
    
    Endereco     = models.CharField(max_length=100, null=True, blank=True)
    Bairro       = models.CharField(max_length=100, null=True, blank=True)
    Cidade       = models.CharField(max_length=100, null=True, blank=True)
    Estado       = models.CharField(max_length=100, null=True, blank=True)
    Cep          = models.CharField(max_length=100, null=True, blank=True)
    Telefones    = models.CharField(max_length=100, null=True, blank=True)
    Email        = models.CharField(max_length=100, null=True, blank=True)
    Extras       = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return self.Nome + ' ' + self.Empresa + ' ' + self.Cpf + ' ' + self.Rg

class HospedeForm(forms.ModelForm):
    
    class Meta:
        model = Hospede

    uuid          = forms.CharField(label="Ref", required=False,
                    widget=forms.TextInput(attrs={'size':35}))
    data_cadastro = forms.DateTimeField(label="Cadastro", required=False)
    
    Nome          = forms.CharField(label="Nome",
                    widget=forms.TextInput(attrs={'size':60}))
    Cpf           = forms.CharField(label="CPF", required=True)
    Rg            = forms.CharField(label="IDENT", required=False)
    Naturalidade  = forms.CharField(label="Naturalidade", required=False,
                    widget=forms.TextInput(attrs={'size':30}))
    Nascimento    = forms.DateTimeField(label="Nascimento", required=False)
    Nacionalidade = forms.CharField(label="Nacionalidade", required=False)
    
    Profissao     = forms.CharField(label="Profissão", required=False,
                    widget=forms.TextInput(attrs={'size':30}))
    Empresa       = forms.CharField(label="Empresa", required=False,
                    widget=forms.TextInput(attrs={'size':60}))
                    
    CarroPlaca    = forms.CharField(label="Placa carro", required=False)
    Procedencia   = forms.CharField(label="Procedencia", required=False)
    Destino       = forms.CharField(label="Destino", required=False)
                    
    Endereco      = forms.CharField(label="Endereço", required=False,
                    widget=forms.TextInput(attrs={'size':60}))
    Bairro        = forms.CharField(label="Bairro", required=False,
                    widget=forms.TextInput(attrs={'size':40}))
    Cidade        = forms.CharField(label="Cidade", required=False,
                    widget=forms.TextInput(attrs={'size':60}))
    Estado        = forms.CharField(label="Estado", required=False)
    Cep           = forms.CharField(label="CEP", required=False)
    Telefones     = forms.CharField(label="Telefone", required=False,
                    widget=forms.TextInput(attrs={'size':35}))
    Email         = forms.CharField(label="E-Mail", required=False)
    #Extras        = forms.Textarea(label="Observações")




    #def clean_referencia(self):
    #    data = self.cleaned_data['referencia']
    #    return rem_acentuacao(data).upper()
    #
    #def clean_categoria(self):
    #    data = self.cleaned_data['categoria']
    #    return rem_acentuacao(data)
    #
    #def clean_descricao(self):
    #    data = self.cleaned_data['descricao']
    #    return rem_acentuacao(data)
    #
    #def clean_fornecedor(self):
    #    data = self.cleaned_data['fornecedor']
    #    return rem_acentuacao(data)


class Hospedagem(models.Model):
    Hospede       = models.ForeignKey(Hospede)
    Apartamento   = models.CharField(max_length=10, null=True)
    NumeroPessoas = models.CharField(max_length=100, null=True)
    Empresa       = models.CharField(max_length=100, null=True)
    Agencia       = models.CharField(max_length=100, null=True)
    DataEntrada   = models.CharField(max_length=100, null=True)
    DataSaida     = models.CharField(max_length=100, null=True)
    ValorDiaria   = models.DecimalField(max_digits=9, decimal_places=2)

class HospedagemForm(forms.ModelForm):
    
    class Meta:
        model = Hospedagem

    Hospede        = forms.CharField(label="Ref", required=True)
    Apartamento   = forms.CharField(label="Apto", required=True)
    NumeroPessoas = forms.CharField(label="Qtd", required=True)
    Empresa       = forms.CharField(label="Emp", required=False)
    Agencia       = forms.CharField(label="Agencia", required=False)
    DataEntrada   = forms.CharField(label="Entr", required=True)
    DataSaida     = forms.CharField(label="Saida", required=True)
    ValorDiaria   = forms.CharField(label="Valor", required=True)



class Empresa(models.Model):

    Empresa         = models.CharField(max_length=100, null=True)
    CNPJ            = models.CharField(max_length=100, null=True)
    IE              = models.CharField(max_length=100, null=True)
    Endereco        = models.CharField(max_length=100, null=True)
    Cidade          = models.CharField(max_length=100, null=True)
    Estado          = models.CharField(max_length=100, null=True)
    CEP             = models.CharField(max_length=100, null=True)
    Contato_Nome    = models.CharField(max_length=100, null=True)
    Contato_Cargo   = models.CharField(max_length=100, null=True)
    Telefone        = models.CharField(max_length=100, null=True)


class Agencia(models.Model):

    Empresa         = models.CharField(max_length=100, null=True)
    CNPJ            = models.CharField(max_length=100, null=True)
    IE              = models.CharField(max_length=100, null=True)
    Endereco        = models.CharField(max_length=100, null=True)
    Cidade          = models.CharField(max_length=100, null=True)
    Estado          = models.CharField(max_length=100, null=True)
    CEP             = models.CharField(max_length=100, null=True)
    Contato_Nome    = models.CharField(max_length=100, null=True)
    Contato_Cargo   = models.CharField(max_length=100, null=True)
    Telefone        = models.CharField(max_length=100, null=True)
    
    