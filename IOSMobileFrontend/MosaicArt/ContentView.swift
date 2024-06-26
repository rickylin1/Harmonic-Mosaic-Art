import SwiftUI

struct ContentView: View {
    
    @State private var mosaic: Mosaic?
    
    var body: some View {
        VStack {
            AsyncImage(url: URL(string: mosaic?.mosaicUrl ?? "")) { image in
                image
                    .image?
                    .resizable()
                    .aspectRatio(contentMode: .fit)
                    .clipShape(Circle())
            }
            Text(mosaic?.albumName ?? "Album Name")
                .bold()
                .font(.largeTitle)
            Text(mosaic?.mosaicUrl ?? "Get a mosaic!")
                .multilineTextAlignment(.center)
        }
        .padding()
        .task {
            await loadMosaic()
        }
    }
    
    func loadMosaic() async {
        do {
            mosaic = try await getMosaic()
        } catch MosaicError.invalidURL {
            print("Invalid URL")
        } catch MosaicError.invalidData {
            print("Invalid Data")
        } catch MosaicError.invalidResponse {
            print("Invalid Response")
        } catch {
            print("Unexpected error: \(error)")
        }
    }
    
    func getMosaic() async throws -> Mosaic {
        let endpoint = "http://127.0.0.1:5000/AlbumCoverMosaic"
        
        guard let url = URL(string: endpoint) else {
            throw MosaicError.invalidURL
        }
        
        let (data, response) = try await URLSession.shared.data(from: url)
        
        guard let httpResponse = response as? HTTPURLResponse, httpResponse.statusCode == 200 else {
            throw MosaicError.invalidResponse
        }
        
        do {
            let decoder = JSONDecoder()
            decoder.keyDecodingStrategy = .convertFromSnakeCase
            return try decoder.decode(Mosaic.self, from: data)
        } catch {
            throw MosaicError.invalidData
        }
    }
}

struct Mosaic: Codable {
    let mosaicUrl: String
    let albumName: String
}

enum MosaicError: Error {
    case invalidURL
    case invalidResponse
    case invalidData
}

#Preview {
    ContentView()
}
