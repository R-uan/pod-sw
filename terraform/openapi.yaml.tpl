openapi: 3.0.4
info:
  title: Star Wars API
  version: 1.0.0

x-google-api-management:
  backends:
    sw_backend:
      address: ${backend_url} 
      pathTranslation: APPEND_PATH_TO_ADDRESS
      protocol: "http/1.1"

x-google-backend: sw_backend

paths:
  /**:
    get:
      summary: Main endpoint
      operationId: getResource
      responses:
        '200':
          description: OK
        '404':
          description: NOT_FOUND
        '400':
          description: BAD_REQUEST
        '500':
          description: INTERNAL_SERVER_ERROR
