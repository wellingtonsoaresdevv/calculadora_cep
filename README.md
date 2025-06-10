<h1 align="center">API de Cálculo de Distância Entre CEPs 🗺️</h1>

<p align="center">
  <img src="https://readme-typing-svg.herokuapp.com?font=Fira+Code&size=22&pause=1000&center=true&vCenter=true&width=435&lines=Distância+Rodoviária+entre+CEPs%F0%9F%9B%A3%EF%B8%8F;Precisão+com+Google+Maps+API%F0%9F%8C%8F;Fallback+Inteligente%F0%9F%9A%80" alt="Typing SVG" />
</p>

---

## 🧠 Sobre a API

🚀 Esta API FastAPI calcula a distância de rota rodoviária (em quilômetros) entre dois CEPs brasileiros.

🛠️ Diferente de cálculos simplificados, ela integra a **Google Distance Matrix API** para distâncias precisas, considerando ruas e estradas.

🎯 Possui um fallback inteligente para a fórmula de Haversine (distância em linha reta) se a API do Google não estiver disponível ou configurada.

---

## ✨ Funcionalidades

* **Cálculo Preciso:** Obtém a distância rodoviária real entre dois CEPs brasileiros usando a Google Distance Matrix API.
* **Fallback Inteligente:** Em caso de problemas com a Google Maps API (chave inválida, cota excedida, etc.), a API automaticamente calcula a distância em linha reta (fórmula de Haversine).
* **Validação de CEP:** Garante que os CEPs fornecidos estejam em um formato válido.
* **Obtenção de Endereço:** Utiliza a API ViaCEP para obter informações detalhadas do endereço a partir do CEP.
* **Retorno Simplificado:** Retorna apenas o CEP de origem, CEP de destino e a distância em quilômetros.

---

## 🚀 Como Usar

### Pré-requisitos

Antes de começar, certifique-se de ter instalado:

* **Python 3.7+**
* **Uma conta no Google Cloud Platform** com a **Distance Matrix API ativada** e o **faturamento configurado**. (Mesmo para o nível gratuito, o faturamento é obrigatório)

---

### 1. Obtenha e Configure sua Chave da Google Maps API

Esta é a etapa mais **CRÍTICA** para que a API funcione corretamente e use o cálculo rodoviário do Google.

<p align="center">
    <strong>PASSO A PASSO NO GOOGLE CLOUD PLATFORM</strong>
</p>
<ol>
    <li><strong>Acesse o Google Cloud Console:</strong>
        <ul>
            <li>Vá para <a href="https://console.cloud.google.com/" target="_blank">console.cloud.google.com</a>.</li>
            <li>Crie um novo projeto ou selecione um existente.</li>
        </ul>
    </li>
    <li><strong>Ative a "Distance Matrix API":</strong>
        <ul>
            <li>No menu lateral, vá em <code>APIs e Serviços</code> &gt; <code>Biblioteca</code>.</li>
            <li>Procure por "Distance Matrix API" e clique em <code>Ativar</code><span class="citation"></span>.</li>
        </ul>
    </li>
    <li><strong>Configure o Faturamento:</strong>
        <ul>
            <li>No menu lateral, vá em <code>Faturamento</code>. Siga as instruções para configurar o faturamento para o seu projeto. É <strong>obrigatório</strong> ter o faturamento ativo, mesmo para usar o nível gratuito da API<span class="citation"></span>.</li>
        </ul>
    </li>
    <li><strong>Crie e Restrinja sua Chave de API:</strong>
        <ul>
            <li>No menu lateral, vá em <code>APIs e Serviços</code> &gt; <code>Credenciais</code>.</li>
            <li>Clique em <code>+ CRIAR CREDENCIAIS</code> e selecione <code>Chave de API</code>.</li>
            <li><strong>COPIE a chave gerada.</strong></li>
            <li><strong>MUITO IMPORTANTE:</strong> Clique em <code>Restringir chave</code> logo após a criação.
                <ul>
                    <li>Em <code>Restrições de aplicativos</code>, considere deixar como "Nenhum" para testes locais. Em produção, restrinja por <code>Endereços IP</code> ou <code>Sites HTTP</code> para aumentar a segurança.</li>
                    <li>Em <code>Restrições de API</code>, selecione <code>Restringir chave</code> e escolha apenas a <strong>"Distance Matrix API"</strong> na lista. Isso impede o uso indevido da sua chave em outras APIs<span class="citation"></span>.</li>
                </ul>
            </li>
        </ul>
    </li>
</ol>

---

### 2. Configuração do Ambiente Local

<p align="center">
    <strong>INSTALANDO E CONFIGURANDO</strong>
</p>
<ol>
    <li><strong>Clone o Repositório (ou baixe o código):</strong>
<pre><code>git clone &lt;URL_DO_SEU_REPOSITORIO&gt;
cd api_drm_distancia_lojas
</code></pre>
    </li>
    <li><strong>Crie um Ambiente Virtual (Recomendado):</strong>
<pre><code>python -m venv venv
</code></pre>
    </li>
    <li><strong>Ative o Ambiente Virtual:</strong>
        <ul>
            <li><strong>Windows (CMD):</strong>
<pre><code>.\venv\Scripts\activate
</code></pre>
            </li>
            <li><strong>Windows (PowerShell):</strong>
<pre><code>.\venv\Scripts\Activate.ps1
</code></pre>
            </li>
            <li><strong>macOS/Linux:</strong>
<pre><code>source venv/bin/activate
</code></pre>
            </li>
        </ul>
    </li>
    <li><strong>Instale as Dependências:</strong>
        <p>Crie um arquivo <code>requirements.txt</code> na raiz do seu projeto com o seguinte conteúdo:</p>
<pre><code>fastapi
uvicorn
requests
geopy
python-dotenv
pydantic
pandas
pgeocode
</code></pre>
        <p>Em seguida, instale-as:</p>
<pre><code>pip install -r requirements.txt
</code></pre>
    </li>
</ol>

---

### 3. Configure a Variável de Ambiente `Maps_API_KEY`

Esta etapa é <strong>fundamental</strong> para que sua API use a chave do Google Maps.

<p align="center">
    <strong>ARMAZENANDO SUA CHAVE DE API COM SEGURANÇA</strong>
</p>
<ul>
    <li><strong>Crie um arquivo <code>.env</code>:</strong> Na <strong>raiz do seu projeto</strong> (na mesma pasta do <code>main.py</code>), crie um arquivo chamado <code>.env</code>.</li>
    <li><strong>Adicione sua chave API ao <code>.env</code>:</strong> Dentro desse arquivo <code>.env</code>, adicione a seguinte linha, substituindo pelo <strong>valor da sua chave real</strong>:
<pre><code>Maps_API_KEY="SUA_CHAVE_DE_API_REAL_E_SEGURA_AQUI"
</code></pre>
        <strong>Exemplo:</strong> <code>Maps_API_KEY="XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"</code>
    </li>
    <li><strong>Adicione <code>.env</code> ao <code>.gitignore</code> (Se usar Git):</strong> Se você estiver usando Git, adicione <code>.env</code> ao seu arquivo <code>.gitignore</code> para evitar que sua chave de API seja enviada para repositórios públicos.
<pre><code># .gitignore
.env
</code></pre>
    </li>
</ul>

---

### 4. Execute a API

<p align="center">
    <strong>COLOCANDO NO AR!</strong>
</p>
<p>Com todas as configurações feitas, execute a API a partir do terminal (com o ambiente virtual ativado):</p>
<pre><code>uvicorn main:app --reload
</code></pre>
<p>Você deverá ver uma mensagem indicando que o Uvicorn está rodando, geralmente em <code>http://127.0.0.1:8000</code>.</p>

---

## 💡 Uso da API

Após iniciar a API, você pode acessa a documentação interativa e testar os endpoints.

### Documentação Interativa (Swagger UI)

<p align="center">
    <strong>EXPLORE A API COM SWAGGER UI</strong>
</p>
<p>Acesse <a href="http://127.0.0.1:8000/docs" target="_blank">http://127.0.0.1:8000/docs</a> no seu navegador. Você verá a interface Swagger UI, onde poderá testar o endpoint <code>/calcular_distancia</code>.</p>
<p align="center">
    <img src="https://i.imgur.com/J8AItZA.png" alt="Exemplo da interface Swagger UI da API">
    <br>
    <small><i>(Adicione aqui uma captura de tela real da sua interface Swagger UI)</i></small>
</p>

### Endpoint de Cálculo de Distância

<p align="center">
    <strong>TESTANDO O CÁLCULO DE DISTÂNCIA</strong>
</p>
<ul>
    <li><strong>GET <code>/calcular_distancia</code></strong>
        <ul>
            <li><strong>Descrição:</strong> Calcula a distância em quilômetros entre dois CEPs brasileiros.</li>
            <li><strong>Parâmetros de Query:</strong>
                <ul>
                    <li><code>cep_origem</code>: CEP de origem (formato: <code>XXXXX-XXX</code> ou <code>XXXXXXXX</code>).</li>
                    <li><code>cep_destino</code>: CEP de destino (formato: <code>XXXXX-XXX</code> ou <code>XXXXXXXX</code>).</li>
                </ul>
            </li>
            <li><strong>Exemplo de Requisição:</strong>
<pre><code>http://127.0.0.1:8000/calcular_distancia?cep_origem=24220-031&amp;cep_destino=01001-000
</code></pre>
            </li>
            <li><strong>Exemplo de Resposta (Sucesso com Google Maps API):</strong>
<pre><code>{
  "cep_origem": "24220-031",
  "cep_destino": "01001-000",
  "distancia_km": 451.23
}
</code></pre>
            </li>
            <li><strong>Exemplo de Resposta (Fallback para Haversine):</strong>
<pre><code>{
  "cep_origem": "24220-031",
  "cep_destino": "01001-000",
  "distancia_km": 367.45
}
</code></pre>
                <div class="warning">
                    <p>Isso ocorrerá se a chave do Google Maps não estiver configurada corretamente ou se houver um erro com a API do Google (por exemplo, faturamento desativado, API não ativada, cota excedida, etc.).</p>
                </div>
            </li>
        </ul>
    </li>
</ul>

---

## 🛠️ Solução de Problemas

<p align="center">
    <strong>PROBLEMAS COM O CÁLCULO? VEJA AQUI!</strong>
</p>
<p>Se você ainda estiver recebendo <code>{"distancia_km": 367.45}</code> ou similar, significa que a API do Google <strong>não está sendo utilizada</strong>. Verifique o console do Uvicorn!</p>

<div class="tip">
    <p><strong>Dica:</strong> No console do Uvicorn, procure por: <code>AVISO: Chave de API do Google Maps não configurada ou inválida. Usando fallback.</code><span class="citation"></span> Se esta mensagem aparecer, o problema é na configuração da sua chave.</p>
</div>

<h3>Possíveis Causas para o Fallback:</h3>
<ol>
    <li><strong>Chave de API Incorreta/Inválida:</strong>
        <ul>
            <li>Você copiou e colou a chave <strong>exatamente</strong> do Google Cloud Console para o seu <code>.env</code>?</li>
            <li>Você <strong>regenerou</strong> a chave se ela foi exposta anteriormente?</li>
            <li>Você se certificou de que não há espaços extras ou caracteres invisíveis no seu <code>.env</code>?</li>
        </ul>
    </li>
    <li><strong>API Não Ativada:</strong>
        <ul>
            <li>Confirme no Google Cloud Console que a <strong>"Distance Matrix API" está ATIVADA</strong> para o seu projeto<span class="citation"></span>.</li>
        </ul>
    </li>
    <li><strong>Faturamento Não Configurado/Ativo:</strong>
        <ul>
            <li>Esta é uma das causas mais comuns! Vá em <code>Faturamento</code> no Google Cloud Console e certifique-se de que está <strong>configurado e ativo</strong>. As APIs não funcionarão sem isso<span class="citation"></span>.</li>
        </ul>
    </li>
    <li><strong>Restrições da Chave Muito Estritas:</strong>
        <ul>
            <li>Se você restringiu sua chave por IP, certifique-se de que o IP da sua máquina local (ou da sua VPS) está permitido. Para testes locais, pode ser mais fácil remover as restrições por IP temporariamente para confirmar se a chave funciona, e depois adicioná-las novamente<span class="citation"></span>.</li>
        </ul>
    </li>
    <li><strong>Variável de Ambiente Não Carregada:</strong>
        <ul>
            <li>Você executou o comando <code>$env:Maps_API_KEY="SUA_CHAVE"</code> (Windows PowerShell) ou <code>export Maps_API_KEY="SUA_CHAVE"</code> (Linux/macOS) <strong>no MESMO terminal</strong> antes de iniciar o <code>uvicorn</code>?</li>
            <li>Se você usa <code>python-dotenv</code> e o arquivo <code>.env</code>, certifique-se de que <code>load_dotenv()</code> está no <strong>início</strong> do seu <code>main.py</code> e que o arquivo <code>.env</code> está na <strong>raiz do projeto</strong>.</li>
            <li><strong>Teste se a variável está visível:</strong> Antes de executar <code>uvicorn</code>, no mesmo terminal, digite <code>$env:Maps_API_KEY</code> (Windows PowerShell) ou <code>echo $Maps_API_KEY</code> (Linux/macOS). Se a sua chave aparecer, a variável está definida.</li>
        </ul>
    </li>
</ol>

---

## 🤝 Contribuindo

<p align="center">
    <strong>COLABORE COM ESTE PROJETO!</strong>
</p>
<p>Contribuições são bem-vindas! Se você tiver sugestões, melhorias ou encontrar bugs, sinta-se à vontade para:</p>
<ol>
    <li>Abrir uma <code>issue</code> descrevendo o problema ou a sugestão.</li>
    <li>Criar um <code>fork</code> do projeto.</li>
    <li>Implementar suas mudanças.</li>
    <li>Abrir um <code>Pull Request</code> explicando suas modificações.</li>
</ol>

---

## 👥 Autores

Este projeto foi desenvolvido por:

* **[Wellington Soares](https://github.com/wellingtonsoaresdevv)**
* **[Fábio Cavalcanti](https://github.com/impacte-ai)**

---

## 📄 Licença

<p align="center">
    <strong>LICENÇA DO PROJETO</strong>
</p>
<p>Este projeto está licenciado sob a licença MIT. Consulte o arquivo <a href="LICENSE"><code>LICENSE</code></a> para mais detalhes.</p>

---

<p align="center">
  <img src="https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/colored.png" width="100%" />
</p>
<p align="center">
  <img src="https://wakatime.com/badge/user/93d6ce54-2e2f-493f-972b-01b78551fc4f.svg" alt="profile views" />
</p>
