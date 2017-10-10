# authenticationService
A simple container for authentication
## To Run:
* Set the following env variables:
  * AUTH_SVC_ROOT_DB_PASS  -- root database password for auth db container
  * AUTH_SVC_DB_NAME  -- db name for auth app
  * AUTH_SVC_DB_USER  -- db username for auth app
  * AUTH_SVC_DB_PASS  -- db password for auth app
  * GOOGLE_OAUTH_CLIENT_ID  -- client id for app registered with google
  * GOOGLE_OAUTH_SECRET  -- google secret for oauth service
  * CURRENT_SERVER_URL  -- url of current server (i.e., http://localhost:8090 OR https://dev-web2.opendmc.org). This is used to manage redirects.
* run ./deploy.sh with 'dev'