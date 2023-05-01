import pygame 
import webbrowser

class Video:
	def __init__(self, title, link):
		self.title = title
		self.link = link
		self.seen = False
	
	def open_vid(self):
		webbrowser.open(self.link)
		print("Opening: " + self.title)
		self.seen = True

class Playlist:
	def __init__(self, name, description, rating, videos):
		self.name = name
		self.description = description
		self.rating = rating
		self.videos = videos

class Text_button:
	def __init__(self, text, pos):
		self.text = text
		self.pos = pos

	def draw(self):
		self.font = pygame.font.SysFont('Comic Sans MS', 30)
		self.text_render = self.font.render(self.text, True, (0,0,255))
		self.text_box = self.text_render.get_rect()
		if self.is_mouse_on_text():
			self.text_render = self.font.render(self.text, True, (0,0,255))
			pygame.draw.line(screen, (0,0,255), (self.pos[0],self.pos[1]+self.text_box[3]),(self.pos[0]+self.text_box[2],self.pos[1]+self.text_box[3]))
		else:
			self.text_render = self.font.render(self.text, True, (0,0,0))	
		self.text_box = self.text_render.get_rect()
		screen.blit(self.text_render, (self.pos[0],self.pos[1]))

	def is_mouse_on_text(self):
		self.mouse_x, self.mouse_y = pygame.mouse.get_pos()
		if ((self.mouse_x>self.pos[0]) and (self.mouse_x<self.pos[0]+self.text_box[2]) and (self.mouse_y>self.pos[1]) and (self.mouse_y<self.pos[1]+self.text_box[3])):
			return True
		else:
			return False
	
	def description_text_box(self, i):
		description_text = playlists[i].description
		des_font = pygame.font.SysFont('Comic Sans MS', 15)
		description_render = des_font.render(description_text, True, (0,0,255))
		description_text_box = description_render.get_rect()
		pygame.draw.rect(screen, (255,255,255), (self.mouse_x, self.mouse_y, description_text_box[2] + 15, description_text_box[3]))
		screen.blit(description_render, (self.mouse_x + 10,self.mouse_y))

	def link_text_box(self, i):
		for j in range(len(playlists)):
			link_text = playlists[j].videos[i].link
		link_font = pygame.font.SysFont('Comic Sans MS', 15)
		link_render = link_font.render(link_text, True, (0,0,255))
		link_text_box = link_render.get_rect()
		pygame.draw.rect(screen, (255,255,255), (self.mouse_x, self.mouse_y, link_text_box[2], link_text_box[3]))
		screen.blit(link_render, (self.mouse_x,self.mouse_y))


def read_playlist_from_txt(file):
	playlist_name = file.readline().rstrip()
	playlist_description = file.readline().rstrip()
	playlist_rating = file.readline().rstrip()
	playlist_videos = read_videos_from_txt(file)
	playlist = Playlist(playlist_name, playlist_description, playlist_rating, playlist_videos)
	return playlist

def	read_playlists_from_txt():
	playlists = []
	with open("data.txt", "r") as file:
		total = file.readline()
		for i in range(int(total)):
			playlist = read_playlist_from_txt(file)
			playlists.append(playlist)
	return playlists

def read_videos_from_txt(file):
	videos = []
	total = file.readline().rstrip()		
	for i in range(int(total)):
		video = read_video_from_txt(file)
		videos.append(video)
	return videos

def read_video_from_txt(file):
	title = file.readline().rstrip()
	link = file.readline().rstrip()
	video = Video(title, link)
	return video

pygame.init()

screen = pygame.display.set_mode((1000,400))
pygame.display.set_caption('MP3 Player')

running = True	
clock = pygame.time.Clock()

MARGIN = 50

playlists = read_playlists_from_txt()
playlists_btn = []
for i in range(len(playlists)):
	playlist_btn = Text_button(playlists[i].name, (50, 50+MARGIN*i))
	playlists_btn.append(playlist_btn)

videos_btn = []

while running:
	screen.fill((255,234,65))
	clock.tick(60)
	
	for playlist_btn in playlists_btn:
		playlist_btn.draw()

	for video_btn in videos_btn:
		video_btn.draw()

	#show description of playlist
	for i in range(len(playlists_btn)):
		if playlists_btn[i].is_mouse_on_text():
			playlists_btn[i].description_text_box(i)
	
	#show link of video
	for i in range (len(videos_btn)):
		if videos_btn[i].is_mouse_on_text():
			videos_btn[i].link_text_box(i)
	
	for event in pygame.event.get():
		if event.type == pygame.MOUSEBUTTONDOWN:
			if event.button == 1:
				for i in range(len(playlists_btn)):
					if playlists_btn[i].is_mouse_on_text():
						playlist_choice = i
						videos_btn = []
						for j in range(len(playlists[i].videos)):
							video_btn = Text_button(playlists[i].videos[j].title, (450, 50+MARGIN*j))
							videos_btn.append(video_btn)
				
				for i in range(len(videos_btn)):
					if videos_btn[i].is_mouse_on_text():
						video_choice = i
						playlists[playlist_choice].videos[i].open_vid()
						
		if event.type == pygame.QUIT:
			running = False

	pygame.display.flip()

pygame.quit()